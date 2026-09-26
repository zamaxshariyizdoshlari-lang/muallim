"""Asosiy mantiq testlari: auth, mavzu ochilishi, ball, streak, takrorlash, qidiruv, tahlil."""
import re
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core import mail
from django.core.cache import cache
from django.test import TestCase
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .models import (
    STATUS_DONE, Book, GeneratedAsset, Lesson, Section, TestAttempt, Topic, TopicCompletion,
)
from .services import gamification

User = get_user_model()
H = '/api/history/'
A = '/api/auth/'


def make_questions(page, n=2):
    return [
        {'question': f'Savol {page}-{i}?', 'options': ['to\'g\'ri', 'xato', 'xato2', 'xato3'],
         'correct_index': 0, 'page': page}
        for i in range(n)
    ]


class CourseFixture(TestCase):
    """2 bo'lim: [t1, t2] va [t3]; har mavzuda 2 savolli test va qidiruv uchun dars."""

    def setUp(self):
        cache.clear()
        self.teacher = User.objects.create_user('ustoz', password='ustoz-parol-1', is_staff=True)
        self.user = User.objects.create_user('talaba', password='talaba-parol-1')
        self.book = Book.objects.create(title='Sinov kursi', key='sinov', uploaded_by=self.teacher)
        s1 = Section.objects.create(book=self.book, key='s1', title='1-bo\'lim', order=1)
        s2 = Section.objects.create(book=self.book, key='s2', title='2-bo\'lim', order=2)
        self.sections = [s1, s2]
        self.topics = []
        for i, (sec, title) in enumerate([(s1, 'Piramidalar'), (s1, 'Nil daryosi'), (s2, 'Yunon polislari')]):
            page = 10 * (i + 1)
            t = Topic.objects.create(
                book=self.book, section=sec, key=f't{i}', title=title,
                start_page=page, end_page=page + 5, order=i,
            )
            GeneratedAsset.objects.create(
                topic=t, created_by=self.teacher, kind=GeneratedAsset.KIND_TOPIC_TEST, status=STATUS_DONE,
                data={'questions': make_questions(page)},
            )
            Lesson.objects.create(
                topic=t, created_by=self.teacher, status=STATUS_DONE,
                lesson_plan={'blocks': [{'heading': 'Kirish', 'pages': [page], 'text': f'{title} haqida matn: fir\'avn.'}],
                             'key_facts': []},
            )
            self.topics.append(t)
        self.client = APIClient()

    def login(self, user):
        token, _ = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

    def submit(self, topic, correct=True):
        answers = {'0': 0 if correct else 1, '1': 0}
        return self.client.post(f'{H}topics/{topic.id}/test/submit/', {'answers': answers}, format='json')


class AuthTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client = APIClient()

    def register(self, **kw):
        data = {'username': 'yangi_talaba', 'password': 'yaxshi-parol-1'}
        data.update(kw)
        return self.client.post(f'{A}register/', data, format='json')

    def test_register_ok_and_login(self):
        r = self.register()
        self.assertEqual(r.status_code, 201)
        self.assertIn('token', r.data)
        r = self.client.post(f'{A}token/', {'username': 'yangi_talaba', 'password': 'yaxshi-parol-1'}, format='json')
        self.assertEqual(r.status_code, 200)

    def test_register_rejects_weak_input(self):
        self.assertEqual(self.register(password='qisqa1').status_code, 400)
        self.assertEqual(self.register(password='12345678').status_code, 400)
        self.assertEqual(self.register(username='ab').status_code, 400)
        self.assertEqual(self.register(email='noto-g-ri').status_code, 400)

    def test_register_duplicate_username_case_insensitive(self):
        self.register()
        self.assertEqual(self.register(username='YANGI_TALABA').status_code, 400)

    def test_password_reset_flow_and_token_rotation(self):
        User.objects.create_user('ali', password='eski-parol-1', email='ali@example.com')
        r = self.client.post(f'{A}password-reset/', {'email': 'ali@example.com'}, format='json')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        m = re.search(r'uid=([^&\s]+)&token=([^&\s]+)', mail.outbox[0].body)
        self.assertIsNotNone(m)
        r = self.client.post(
            f'{A}password-reset/confirm/',
            {'uid': m.group(1), 'token': m.group(2), 'password': 'yangi-parol-2'}, format='json',
        )
        self.assertEqual(r.status_code, 200)
        self.assertTrue(User.objects.get(username='ali').check_password('yangi-parol-2'))
        # token bir martalik
        r = self.client.post(
            f'{A}password-reset/confirm/',
            {'uid': m.group(1), 'token': m.group(2), 'password': 'boshqa-parol-3'}, format='json',
        )
        self.assertEqual(r.status_code, 400)

    def test_password_reset_does_not_reveal_unknown_email(self):
        r = self.client.post(f'{A}password-reset/', {'email': 'yoq@example.com'}, format='json')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(mail.outbox), 0)

    def test_change_password_rotates_token(self):
        u = User.objects.create_user('vali', password='eski-parol-1')
        old = Token.objects.create(user=u).key
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {old}')
        r = self.client.post(
            f'{A}change-password/', {'old_password': 'eski-parol-1', 'new_password': 'yangi-parol-2'}, format='json')
        self.assertEqual(r.status_code, 200)
        self.assertNotEqual(r.data['token'], old)
        self.assertFalse(Token.objects.filter(key=old).exists())

    def test_change_password_wrong_old(self):
        u = User.objects.create_user('vali', password='eski-parol-1')
        self.client.force_authenticate(u)
        r = self.client.post(
            f'{A}change-password/', {'old_password': 'xato', 'new_password': 'yangi-parol-2'}, format='json')
        self.assertEqual(r.status_code, 400)

    def test_api_requires_auth(self):
        self.assertEqual(self.client.get(f'{H}subjects/').status_code, 401)


class UnlockTests(CourseFixture):
    def test_second_topic_locked_until_first_passed(self):
        self.login(self.user)
        t1, t2, _ = self.topics
        self.assertEqual(self.submit(t2).status_code, 403)
        r = self.submit(t1, correct=False)
        self.assertEqual(r.status_code, 200)
        self.assertFalse(r.data['passed'])
        self.assertEqual(self.submit(t2).status_code, 403)
        self.assertTrue(self.submit(t1).data['passed'])
        self.assertEqual(self.submit(t2).status_code, 200)

    def test_next_section_needs_section_exam(self):
        self.login(self.user)
        t1, t2, t3 = self.topics
        self.submit(t1)
        self.submit(t2)
        # 1-bo'lim testi topshirilmagan: 3-mavzu yopiq
        self.assertEqual(self.submit(t3).status_code, 403)

    def test_teacher_has_everything_unlocked(self):
        self.login(self.teacher)
        self.assertEqual(self.submit(self.topics[2]).status_code, 200)

    def test_student_never_sees_correct_index(self):
        self.login(self.user)
        r = self.client.get(f'{H}topics/{self.topics[0].id}/assets/topic_test/')
        self.assertEqual(r.status_code, 200)
        self.assertNotIn('correct_index', str(r.data))

    def test_result_does_not_leak_answers(self):
        self.login(self.user)
        r = self.submit(self.topics[0], correct=False)
        self.assertNotIn('correct_index', str(r.data))

    def test_progress_reports_unlocked_state(self):
        self.login(self.user)
        r = self.client.get(f'{H}books/{self.book.id}/progress/')
        self.assertEqual(r.status_code, 200)


class GamificationTests(CourseFixture):
    def test_xp_awarded_once(self):
        self.login(self.user)
        first = self.submit(self.topics[0]).data['xp_gained']
        self.assertEqual(first, gamification.POINTS['topic'] + gamification.POINTS['topic_first'])
        self.assertEqual(self.submit(self.topics[0]).data['xp_gained'], 0)
        self.assertEqual(gamification.total_xp(self.user), first)

    def test_no_first_attempt_bonus_after_failure(self):
        self.login(self.user)
        self.submit(self.topics[0], correct=False)
        self.assertEqual(self.submit(self.topics[0]).data['xp_gained'], gamification.POINTS['topic'])

    def test_level_info(self):
        self.assertEqual(gamification.level_info(0)['level'], 1)
        self.assertEqual(gamification.level_info(199)['level'], 1)
        self.assertEqual(gamification.level_info(200)['level'], 2)
        self.assertEqual(gamification.level_info(200)['xp_in_level'], 0)

    def _attempt_on(self, days_ago):
        a = TestAttempt.objects.create(
            student=self.user, topic=self.topics[0], answers={}, score=0, total=2, passed=False)
        TestAttempt.objects.filter(pk=a.pk).update(created_at=timezone.now() - timedelta(days=days_ago))

    def test_streak_counts_consecutive_days(self):
        for d in (0, 1, 2, 5):
            self._attempt_on(d)
        s = gamification.streak_info(self.user)
        self.assertEqual(s['current'], 3)
        self.assertEqual(s['best'], 3)
        self.assertTrue(s['active_today'])

    def test_streak_survives_until_end_of_today(self):
        self._attempt_on(1)
        s = gamification.streak_info(self.user)
        self.assertEqual(s['current'], 1)
        self.assertFalse(s['active_today'])

    def test_streak_broken_after_gap(self):
        self._attempt_on(3)
        self.assertEqual(gamification.streak_info(self.user)['current'], 0)

    def test_first_step_badge(self):
        self.login(self.user)
        self.submit(self.topics[0])
        earned = {b['key'] for b in gamification.badges(self.user) if b['earned']}
        self.assertIn('first_step', earned)
        self.assertEqual(TopicCompletion.objects.filter(student=self.user).count(), 1)


class ReviewSearchTests(CourseFixture):
    def test_wrong_answer_enters_review_and_is_removed_when_answered(self):
        self.login(self.user)
        self.submit(self.topics[0], correct=False)
        items = self.client.get(f'{H}books/{self.book.id}/review/').data['items']
        self.assertEqual(len(items), 1)
        self.assertNotIn('correct_index', items[0])
        url = f'{H}books/{self.book.id}/review/answer/'
        r = self.client.post(url, {'key': items[0]['key'], 'choice': 1}, format='json')
        self.assertFalse(r.data['correct'])
        self.assertEqual(r.data['xp_gained'], 0)
        r = self.client.post(url, {'key': items[0]['key'], 'choice': 0}, format='json')
        self.assertTrue(r.data['correct'])
        self.assertEqual(r.data['xp_gained'], gamification.POINTS['review'])
        self.assertEqual(self.client.get(f'{H}books/{self.book.id}/review/').data['items'], [])

    def test_review_unknown_key_rejected(self):
        self.login(self.user)
        r = self.client.post(
            f'{H}books/{self.book.id}/review/answer/', {'key': 'yoq', 'choice': 0}, format='json')
        self.assertEqual(r.status_code, 400)

    def test_search_limited_to_unlocked_topics(self):
        self.login(self.user)
        hits = self.client.get(f'{H}books/{self.book.id}/search/', {'q': 'fir\'avn'}).data['results']
        self.assertEqual([h['topic_id'] for h in hits], [self.topics[0].id])
        self.login(self.teacher)
        hits = self.client.get(f'{H}books/{self.book.id}/search/', {'q': 'fir\'avn'}).data['results']
        self.assertEqual(len(hits), 3)

    def test_search_short_query_returns_nothing(self):
        self.login(self.user)
        self.assertEqual(self.client.get(f'{H}books/{self.book.id}/search/', {'q': 'a'}).data['results'], [])


class PermissionTests(CourseFixture):
    def test_analytics_teacher_only(self):
        self.login(self.user)
        self.assertEqual(self.client.get(f'{H}books/{self.book.id}/analytics/').status_code, 403)
        self.login(self.teacher)
        r = self.client.get(f'{H}books/{self.book.id}/analytics/')
        self.assertEqual(r.status_code, 200)
        self.assertIn('summary', r.data)

    def test_student_cannot_import_or_create_exam(self):
        self.login(self.user)
        self.assertEqual(self.client.post(f'{H}books/{self.book.id}/exam/create/').status_code, 403)

    def test_profile_and_me(self):
        self.login(self.user)
        p = self.client.get(f'{H}profile/')
        self.assertEqual(p.status_code, 200)
        self.assertEqual(p.data['level'], 1)
        r = self.client.patch(f'{H}me/', {'first_name': 'Ali'}, format='json')
        self.assertEqual(r.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Ali')


class HealthTests(TestCase):
    def test_health_public(self):
        r = self.client.get('/api/health/')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['status'], 'ok')
