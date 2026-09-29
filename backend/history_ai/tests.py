"""Asosiy mantiq testlari: auth, mavzu ochilishi, ball, streak, takrorlash, qidiruv, tahlil."""
import json
import re
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core import mail
from django.core.cache import cache
from django.test import TestCase, override_settings
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
        answers = {'0': "to'g'ri" if correct else 'xato', '1': "to'g'ri"}
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
        self.assertEqual(
            first, gamification.POINTS['topic'] + gamification.POINTS['topic_first'] + gamification.POINTS['topic_perfect']
        )
        self.assertEqual(self.submit(self.topics[0]).data['xp_gained'], 0)
        self.assertEqual(gamification.total_xp(self.user), first)

    def test_no_first_attempt_bonus_after_failure(self):
        self.login(self.user)
        self.submit(self.topics[0], correct=False)
        self.assertEqual(
            self.submit(self.topics[0]).data['xp_gained'],
            gamification.POINTS['topic'] + gamification.POINTS['topic_perfect'],
        )

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

    def test_wrong_test_answer_includes_explanation(self):
        self.login(self.user)
        r = self.submit(self.topics[0], correct=False)
        wrong = next(d for d in r.data['details'] if not d['correct'])
        self.assertIsNotNone(wrong['explain'])
        self.assertIn('heading', wrong['explain'])

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

    def test_dictionary_limited_to_unlocked_topics_and_filters_by_query(self):
        from .models import Lesson
        Lesson.objects.filter(topic=self.topics[0]).update(
            lesson_plan={'blocks': [{'text': 'x'}], 'vocabulary': [{'tr': 'merhaba', 'uz': "salom"}]}
        )
        Lesson.objects.filter(topic=self.topics[1]).update(
            lesson_plan={'blocks': [{'text': 'x'}], 'vocabulary': [{'tr': 'günaydın', 'uz': 'xayrli tong'}]}
        )
        self.login(self.user)
        items = self.client.get(f'{H}books/{self.book.id}/dictionary/').data['items']
        self.assertEqual([w['tr'] for w in items], ['merhaba'])

        self.submit(self.topics[0])
        items = self.client.get(f'{H}books/{self.book.id}/dictionary/').data['items']
        self.assertEqual(sorted(w['tr'] for w in items), ['günaydın', 'merhaba'])

        items = self.client.get(f'{H}books/{self.book.id}/dictionary/', {'q': 'salom'}).data['items']
        self.assertEqual([w['tr'] for w in items], ['merhaba'])


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


class DataBackupTests(TestCase):
    def test_disabled_without_token_setting(self):
        with override_settings(BACKUP_TOKEN=''):
            r = self.client.get(f'{H}backup/')
        self.assertEqual(r.status_code, 404)

    def test_rejects_missing_or_wrong_token(self):
        with override_settings(BACKUP_TOKEN='sirli-token'):
            self.assertEqual(self.client.get(f'{H}backup/').status_code, 403)
            r = self.client.get(f'{H}backup/', HTTP_X_BACKUP_TOKEN='notogri')
            self.assertEqual(r.status_code, 403)

    def test_accepts_correct_token_and_returns_json_dump(self):
        User.objects.create_user('zaxirauser', password='zaxira-parol-1')
        with override_settings(BACKUP_TOKEN='sirli-token'):
            r = self.client.get(f'{H}backup/', HTTP_X_BACKUP_TOKEN='sirli-token')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r['Content-Type'], 'application/json')
        self.assertIn('attachment', r['Content-Disposition'])
        data = json.loads(r.content)
        self.assertTrue(any(obj['model'] == 'auth.user' for obj in data))


class DailyGoalLeaderboardTests(CourseFixture):
    def test_daily_goal_progress_and_settings(self):
        self.login(self.user)
        d = self.client.get(f'{H}profile/').data['daily']
        self.assertEqual((d['goal'], d['today'], d['met']), (50, 0, False))
        self.submit(self.topics[0])  # +70
        self.assertTrue(self.client.get(f'{H}profile/').data['daily']['met'])
        r = self.client.patch(f'{H}me/', {'daily_goal': 100}, format='json')
        self.assertEqual(r.data['daily_goal'], 100)
        self.assertFalse(self.client.get(f'{H}profile/').data['daily']['met'])
        self.assertEqual(self.client.patch(f'{H}me/', {'daily_goal': 7}, format='json').status_code, 400)

    def test_leaderboard_ranks_and_opt_out(self):
        other = User.objects.create_user('boshqa', password='boshqa-parol-1', first_name='Vali')
        self.login(self.user)
        self.submit(self.topics[0])
        self.login(other)
        r = self.client.get(f'{H}leaderboard/')
        self.assertEqual([t['name'] for t in r.data['top']], ['talaba'])
        self.assertIsNone(r.data['me'])
        self.login(self.user)
        self.assertEqual(self.client.get(f'{H}leaderboard/').data['me']['rank'], 1)
        self.client.patch(f'{H}me/', {'show_in_leaderboard': False}, format='json')
        self.assertEqual(self.client.get(f'{H}leaderboard/').data['top'], [])


class QuestionTypesTests(CourseFixture):
    """fill_blank va ordering savol turlari: baholash va javob yashirish."""

    def _make_test(self, topic):
        GeneratedAsset.objects.filter(topic=topic, kind=GeneratedAsset.KIND_TOPIC_TEST).update(
            data={'questions': [
                {'type': 'mcq', 'question': 'Poytaxt?', 'options': ['Toshkent', 'Samarqand'], 'correct_index': 0},
                {'type': 'fill_blank', 'question': "1991-yil nima bo'ldi?", 'answer': 'Mustaqillik'},
                {'type': 'ordering', 'question': "Tartibla", 'items': ['Birinchi', 'Ikkinchi', 'Uchinchi']},
            ]},
        )

    def test_student_never_sees_answers_for_new_types(self):
        self.login(self.user)
        self._make_test(self.topics[0])
        r = self.client.get(f'{H}topics/{self.topics[0].id}/assets/topic_test/')
        body = str(r.data)
        self.assertNotIn('Mustaqillik', body)
        self.assertNotIn('correct_index', body)
        # ordering elementlari hali ham mavjud (faqat tartibi aralashgan bo'lishi mumkin)
        for item in ['Birinchi', 'Ikkinchi', 'Uchinchi']:
            self.assertIn(item, body)

    def test_grading_fill_blank_case_and_whitespace_insensitive(self):
        self.login(self.user)
        self._make_test(self.topics[0])
        r = self.client.post(f'{H}topics/{self.topics[0].id}/test/submit/', {'answers': {
            '0': 'Toshkent', '1': '  mustaqillik  ', '2': ['Birinchi', 'Ikkinchi', 'Uchinchi'],
        }}, format='json')
        self.assertEqual(r.data['score'], 3)
        self.assertTrue(r.data['passed'])

    def test_grading_ordering_wrong_order_fails(self):
        self.login(self.user)
        self._make_test(self.topics[0])
        r = self.client.post(f'{H}topics/{self.topics[0].id}/test/submit/', {'answers': {
            '0': 'Toshkent', '1': 'Mustaqillik', '2': ['Ikkinchi', 'Birinchi', 'Uchinchi'],
        }}, format='json')
        self.assertEqual(r.data['score'], 2)
        self.assertEqual(r.data['details'][2]['correct_answer'], ['Birinchi', 'Ikkinchi', 'Uchinchi'])


class FriendsTests(CourseFixture):
    def setUp(self):
        super().setUp()
        self.other = User.objects.create_user('doston', password='doston-parol-1', first_name='Doston')

    def test_request_accept_and_list(self):
        self.login(self.user)
        r = self.client.post(f'{H}friends/request/', {'username': 'doston'}, format='json')
        self.assertEqual(r.status_code, 201)
        self.assertEqual(self.client.get(f'{H}friends/').data['outgoing'], [{'username': 'doston', 'name': 'Doston'}])

        self.login(self.other)
        incoming = self.client.get(f'{H}friends/').data['incoming']
        self.assertEqual(incoming, [{'username': 'talaba', 'name': 'talaba'}])
        r = self.client.post(f'{H}friends/accept/', {'username': 'talaba'}, format='json')
        self.assertEqual(r.status_code, 200)
        self.assertEqual([f['username'] for f in r.data['friends']], ['talaba'])

        self.login(self.user)
        self.assertEqual([f['username'] for f in self.client.get(f'{H}friends/').data['friends']], ['doston'])

    def test_cannot_request_self_or_duplicate(self):
        self.login(self.user)
        r = self.client.post(f'{H}friends/request/', {'username': 'talaba'}, format='json')
        self.assertEqual(r.status_code, 400)
        self.client.post(f'{H}friends/request/', {'username': 'doston'}, format='json')
        r = self.client.post(f'{H}friends/request/', {'username': 'doston'}, format='json')
        self.assertEqual(r.status_code, 400)

    def test_decline_and_remove(self):
        self.login(self.user)
        self.client.post(f'{H}friends/request/', {'username': 'doston'}, format='json')
        self.login(self.other)
        self.client.post(f'{H}friends/decline/', {'username': 'talaba'}, format='json')
        self.assertEqual(self.client.get(f'{H}friends/').data['incoming'], [])

        self.login(self.user)
        self.client.post(f'{H}friends/request/', {'username': 'doston'}, format='json')
        self.login(self.other)
        self.client.post(f'{H}friends/accept/', {'username': 'talaba'}, format='json')
        self.client.post(f'{H}friends/remove/', {'username': 'talaba'}, format='json')
        self.assertEqual(self.client.get(f'{H}friends/').data['friends'], [])


class StreakFreezeTests(CourseFixture):
    def _active(self, days_ago_list):
        for d in days_ago_list:
            a = TestAttempt.objects.create(
                student=self.user, topic=self.topics[0], answers={}, score=0, total=2, passed=False)
            TestAttempt.objects.filter(pk=a.pk).update(created_at=timezone.now() - timedelta(days=d))

    def test_freeze_earned_after_seven_days_forgives_one_gap(self):
        # 8..2 kun oldin faol (7 kun -> 1 muzlatish), 1 kun oldin o'tkazilgan, bugun faol
        self._active([8, 7, 6, 5, 4, 3, 2, 0])
        s = gamification.streak_info(self.user)
        self.assertEqual(s['current'], 8)
        self.assertEqual(s['freezes'], 0)

    def test_no_freeze_breaks_streak(self):
        self._active([3, 2, 0])
        self.assertEqual(gamification.streak_info(self.user)['current'], 1)

    def test_freeze_counted_in_inventory(self):
        self._active([6, 5, 4, 3, 2, 1, 0])
        s = gamification.streak_info(self.user)
        self.assertEqual((s['current'], s['freezes']), (7, 1))

    def test_review_answer_counts_as_activity(self):
        from .models import ReviewAnswer
        ReviewAnswer.objects.create(user=self.user, book=self.book, qkey='abc', correct=True)
        self.assertTrue(gamification.streak_info(self.user)['active_today'])


class SpacedRepetitionTests(CourseFixture):
    """review.INTERVALS = [1, 3, 7, 14, 30]: har to'g'ri javob keyingi intervalga o'tkazadi."""

    def _card_key(self):
        from .services.review import qkey
        return qkey(self.topics[0].assets.first().data['questions'][0]['question'])

    def test_interval_grows_and_card_is_mastered_at_the_end(self):
        from .models import ReviewCard
        from .services.review import INTERVALS
        self.login(self.user)
        self.submit(self.topics[0], correct=False)
        key = self._card_key()
        url = f'{H}books/{self.book.id}/review/answer/'
        for expected_next in INTERVALS[1:]:
            r = self.client.post(url, {'key': key, 'choice': 0}, format='json')
            self.assertTrue(r.data['correct'])
            self.assertEqual(r.data['next_in_days'], expected_next)
            self.assertFalse(r.data['mastered'])
        r = self.client.post(url, {'key': key, 'choice': 0}, format='json')
        self.assertTrue(r.data['mastered'])
        self.assertIsNone(r.data['next_in_days'])
        self.assertFalse(ReviewCard.objects.filter(qkey=key).exists())

    def test_wrong_answer_resets_interval_to_due_today(self):
        self.login(self.user)
        self.submit(self.topics[0], correct=False)
        key = self._card_key()
        url = f'{H}books/{self.book.id}/review/answer/'
        self.client.post(url, {'key': key, 'choice': 0}, format='json')  # ilgarilaydi (3 kun)
        self.assertEqual(self.client.get(f'{H}books/{self.book.id}/review/').data['items'], [])
        r = self.client.post(url, {'key': key, 'choice': 1}, format='json')  # xato -> darhol qaytadi
        self.assertFalse(r.data['correct'])
        self.assertEqual(len(self.client.get(f'{H}books/{self.book.id}/review/').data['items']), 1)

    def test_section_exam_wrong_answer_creates_card_with_topic(self):
        from .models import SectionExam, ReviewCard
        SectionExam.objects.create(section=self.sections[0], data={'questions': make_questions(10, n=2)})
        self.login(self.user)
        self.submit(self.topics[0])
        self.submit(self.topics[1])
        r = self.client.post(
            f'{H}sections/{self.sections[0].id}/exam/submit/', {'answers': {'0': 'xato', '1': "to'g'ri"}}, format='json')
        self.assertEqual(r.status_code, 200)
        card = ReviewCard.objects.get(user=self.user, book=self.book, qkey=qkey_of('Savol 10-0?'))
        self.assertEqual(card.data['topic_id'], self.topics[0].id)


def qkey_of(text):
    from .services.review import qkey
    return qkey(text)


class CertificateVerifyTests(CourseFixture):
    def _earn_certificate(self):
        from .models import BookExam, SectionCompletion, TopicCompletion
        for t in self.topics:
            TopicCompletion.objects.create(student=self.user, topic=t)
        for s in self.sections:
            SectionCompletion.objects.create(student=self.user, section=s)
        BookExam.objects.create(
            book=self.book, created_by=self.teacher, status=STATUS_DONE,
            data={'questions': make_questions(99, n=1)},
        )
        self.login(self.user)
        return self.client.post(f'{H}books/{self.book.id}/exam/submit/', {'answers': {'0': "to'g'ri"}}, format='json')

    def test_certificate_verify_public_and_unknown_code(self):
        from .models import Certificate
        r = self._earn_certificate()
        self.assertTrue(r.data['certificate'])
        cert = Certificate.objects.get(student=self.user, book=self.book)
        self.assertTrue(cert.code)
        anon = APIClient()
        ok = anon.get(f'/api/history/certificates/verify/{cert.code}/')
        self.assertEqual(ok.status_code, 200)
        self.assertTrue(ok.data['valid'])
        self.assertEqual(ok.data['book_title'], self.book.title)
        missing = anon.get('/api/history/certificates/verify/NOSUCHCODE/')
        self.assertEqual(missing.status_code, 404)
        self.assertFalse(missing.data['valid'])


class IntroTopicUnlockTests(TestCase):
    """"Kirish" mavzusi bo'lsa, undan keyingi mavzu ham darhol ochiq bo'lishi kerak."""

    def setUp(self):
        cache.clear()
        self.teacher = User.objects.create_user('ustoz2', password='ustoz-parol-1', is_staff=True)
        self.user = User.objects.create_user('talaba2', password='talaba-parol-1')
        self.book = Book.objects.create(title='Kirishli kurs', key='kirishli', uploaded_by=self.teacher)
        self.topics = [
            Topic.objects.create(book=self.book, key='k', title='Kirish', start_page=1, end_page=2, order=0),
            Topic.objects.create(book=self.book, key='t1', title='1-§. Birinchi', start_page=3, end_page=4, order=1),
            Topic.objects.create(book=self.book, key='t2', title='2-§. Ikkinchi', start_page=5, end_page=6, order=2),
        ]

    def test_topic_after_intro_is_unlocked_without_finishing_intro(self):
        from .progress import topic_states
        states = topic_states(self.user, self.topics)
        kirish, first, second = self.topics
        self.assertTrue(states[kirish.id]['unlocked'])
        self.assertTrue(states[first.id]['unlocked'])
        self.assertFalse(states[second.id]['unlocked'])

    def test_topic_after_first_real_topic_still_gated(self):
        from .progress import topic_states
        from .models import TopicCompletion
        _, first, second = self.topics
        TopicCompletion.objects.create(student=self.user, topic=first)
        states = topic_states(self.user, self.topics)
        self.assertTrue(states[second.id]['unlocked'])

    def test_without_intro_normal_gating_applies(self):
        from .progress import topic_states
        plain = [
            Topic.objects.create(book=self.book, key='a', title='1-§. A', start_page=10, end_page=11, order=10),
            Topic.objects.create(book=self.book, key='b', title='2-§. B', start_page=12, end_page=13, order=11),
        ]
        states = topic_states(self.user, plain)
        self.assertTrue(states[plain[0].id]['unlocked'])
        self.assertFalse(states[plain[1].id]['unlocked'])


class AdminStatsTests(CourseFixture):
    def test_platform_overview_counts(self):
        from .services.admin_stats import platform_overview
        self.login(self.user)
        self.submit(self.topics[0])
        o = platform_overview()
        self.assertEqual(o['students_total'], 1)  # teacher is_staff=True -> hisoblanmaydi
        self.assertEqual(o['students_active_today'], 1)
        self.assertEqual(o['new_registrations_7d'], 1)
        self.assertEqual(o['books_total'], 1)
        self.assertEqual(o['most_popular_book'], self.book.title)
        self.assertEqual(o['certificates_total'], 0)

    def test_platform_overview_empty_when_no_activity(self):
        from .services.admin_stats import platform_overview
        o = platform_overview()
        self.assertEqual(o['students_total'], 1)
        self.assertEqual(o['students_active_today'], 0)
        self.assertIsNone(o['most_popular_book'])


class AdminContentCreationTests(CourseFixture):
    """Admin panel orqali JSON import'siz yangi fan/kurs yaratish."""

    def test_create_subject_and_book_requires_staff(self):
        self.login(self.user)
        r = self.client.post(f'{H}admin/subjects/', {'slug': 'fizika', 'title': 'Fizika'}, format='json')
        self.assertEqual(r.status_code, 403)

    def test_teacher_creates_subject_then_book(self):
        self.login(self.teacher)
        r = self.client.post(f'{H}admin/subjects/', {'slug': 'fizika', 'title': 'Fizika'}, format='json')
        self.assertEqual(r.status_code, 201)
        subject_id = r.data['id']

        r = self.client.post(f'{H}admin/books/', {'title': '7-sinf Fizika', 'subject': subject_id}, format='json')
        self.assertEqual(r.status_code, 201, r.data)
        from .models import Book
        book = Book.objects.get(id=r.data['id'])
        self.assertEqual(book.uploaded_by, self.teacher)
        self.assertTrue(book.key)
        self.assertEqual(book.subject_id, subject_id)


class StudentGroupTests(CourseFixture):
    def test_teacher_creates_group_and_adds_student(self):
        self.login(self.teacher)
        r = self.client.post(f'{H}admin/groups/', {'name': "9-A sinf"}, format='json')
        self.assertEqual(r.status_code, 201, r.data)
        group_id = r.data['id']

        r = self.client.post(f'{H}admin/groups/{group_id}/members/', {'username': 'talaba'}, format='json')
        self.assertEqual(r.status_code, 201)

        r = self.client.get(f'{H}admin/groups/{group_id}/')
        self.assertEqual([s['username'] for s in r.data['students']], ['talaba'])

        r = self.client.get(f'{H}admin/students/?group={group_id}')
        self.assertEqual([s['username'] for s in r.data], ['talaba'])

    def test_group_scoped_to_owning_teacher(self):
        other_teacher = User.objects.create_user('boshqa_ustoz', password='parol-12345', is_staff=True)
        self.login(self.teacher)
        r = self.client.post(f'{H}admin/groups/', {'name': "9-A sinf"}, format='json')
        group_id = r.data['id']

        self.login(other_teacher)
        self.assertEqual(self.client.get(f'{H}admin/groups/{group_id}/').status_code, 404)
        self.assertEqual(self.client.get(f'{H}admin/groups/').data, [])

    def test_remove_member(self):
        self.login(self.teacher)
        group_id = self.client.post(f'{H}admin/groups/', {'name': 'G'}, format='json').data['id']
        self.client.post(f'{H}admin/groups/{group_id}/members/', {'username': 'talaba'}, format='json')
        r = self.client.delete(f'{H}admin/groups/{group_id}/members/{self.user.id}/')
        self.assertEqual(r.status_code, 204)
        self.assertEqual(self.client.get(f'{H}admin/groups/{group_id}/').data['students'], [])


class LanguageContentImportTests(TestCase):
    """Til kursi uchun ixtiyoriy maydonlar (vocabulary/listening/sentence_practice/...) import qilinishi."""

    def setUp(self):
        self.user = User.objects.create_user('admin_test', password='admin-parol-1', is_staff=True)

    def _base_topic(self, **extra_explanation):
        return {
            'format_version': 1,
            'book': {'key': 'til_sinov', 'title': 'Til sinov kursi', 'subject': 'sinov-tili'},
            'sections': [{
                'key': 's1', 'title': "1-bo'lim", 'topics': [{
                    'key': 't1', 'title': '1-dars', 'start_page': 1, 'end_page': 2,
                    'explanation': {
                        'blocks': [{'heading': 'Grammatika', 'text': 'Qoida matni.'}],
                        **extra_explanation,
                    },
                    'test': make_questions(1, n=5),
                }],
            }],
        }

    def test_language_fields_pass_through_to_lesson_plan(self):
        from .services.book_import import import_book_json
        from .models import Lesson, Topic
        data = self._base_topic(
            vocabulary=[{'tr': 'merhaba', 'uz': 'salom', 'example_tr': 'Merhaba!', 'example_uz': 'Salom!'}],
            listening={
                'dialogue': [{'speaker': 'Ali', 'text': 'Merhaba!'}],
                'questions': [{'question': 'Kim gapirdi?', 'options': ['Ali', 'Vali'], 'correct_index': 0, 'page': 1}],
            },
            sentence_practice=[
                {'type': 'choice', 'prompt': 'Salom?', 'options': ['Merhaba', 'Hayır'], 'correct_index': 0},
                {'type': 'order', 'prompt': 'Tuzing', 'words': ['Benim', 'adım', 'Ali.']},
            ],
            reading={
                'title': 'Sinfda', 'text': 'Bugün yeni bir öğrenci var.',
                'questions': [{'question': 'Kim yangi?', 'options': ['Öğrenci', 'Öğretmen'], 'correct_index': 0}],
            },
            writing_prompt={'instruction': 'Yozing', 'sample_answer': 'Merhaba!'},
            speaking_prompt={'sentences': ['Merhaba!']},
        )
        import_book_json(data, self.user)
        topic = Topic.objects.get(key='t1')
        plan = Lesson.objects.get(topic=topic).lesson_plan
        self.assertEqual(plan['vocabulary'][0]['tr'], 'merhaba')
        self.assertEqual(plan['listening']['dialogue'][0]['speaker'], 'Ali')
        self.assertEqual(plan['reading']['title'], 'Sinfda')
        self.assertEqual(len(plan['sentence_practice']), 2)
        self.assertEqual(plan['writing_prompt']['instruction'], 'Yozing')
        self.assertEqual(plan['speaking_prompt']['sentences'], ['Merhaba!'])

    def test_history_topics_unaffected_without_language_fields(self):
        from .services.book_import import import_book_json
        from .models import Lesson, Topic
        import_book_json(self._base_topic(), self.user)
        plan = Lesson.objects.get(topic=Topic.objects.get(key='t1')).lesson_plan
        self.assertNotIn('vocabulary', plan)
        self.assertNotIn('listening', plan)

    def test_invalid_sentence_practice_type_rejected(self):
        from .services.book_import import validate_book_json
        data = self._base_topic(sentence_practice=[{'type': 'unknown', 'words': ['a', 'b']}])
        errors = validate_book_json(data)
        self.assertTrue(any('sentence_practice' in e for e in errors))

    def test_vocabulary_missing_fields_rejected(self):
        from .services.book_import import validate_book_json
        data = self._base_topic(vocabulary=[{'tr': 'merhaba'}])
        errors = validate_book_json(data)
        self.assertTrue(any('vocabulary' in e for e in errors))

    def test_reading_without_text_rejected(self):
        from .services.book_import import validate_book_json
        data = self._base_topic(reading={'title': 'Sarlavha', 'questions': []})
        errors = validate_book_json(data)
        self.assertTrue(any('reading' in e for e in errors))

    def test_mcq_page_is_optional(self):
        """page berilmasa ham xato bo'lmasin (til kursida bet raqami yo'q)."""
        from .services.book_import import validate_book_json
        data = self._base_topic(
            sentence_practice=[{'type': 'choice', 'prompt': 'S?', 'options': ['A', 'B'], 'correct_index': 0}],
        )
        errors = validate_book_json(data)
        self.assertEqual(errors, [])
