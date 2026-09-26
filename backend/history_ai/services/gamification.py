"""ball, daraja, kunlik ketma-ketlik (streak) va nishonlar.

ball jurnali (XPEvent) bir marta beriladi (user+kind+ref unikal), shuning uchun testni qayta
topshirish XPni ko'paytirmaydi. Streak va nishonlar mavjud ma'lumotlardan hisoblanadi.
"""
from datetime import timedelta

from django.db.models import Count, Sum
from django.utils import timezone

from ..models import Certificate, SectionCompletion, TestAttempt, TopicCompletion, XPEvent

POINTS = {'topic': 50, 'topic_first': 20, 'section': 150, 'exam': 300, 'review': 5}
XP_PER_LEVEL = 200

LEVEL_TITLES = ['Yangi o\'quvchi', 'Izlanuvchi', 'Bilimdon', 'Donishmand', 'Alloma', 'Ustoz']


def _award(user, kind, ref_id, points):
    _, created = XPEvent.objects.get_or_create(
        user=user, kind=kind, ref_id=ref_id, defaults={'points': points}
    )
    return points if created else 0


def award_topic(user, topic):
    """Mavzu testi 100% topshirilganda: asosiy ball + birinchi urinishda bo'lsa bonus."""
    gained = _award(user, 'topic', topic.id, POINTS['topic'])
    if gained and TestAttempt.objects.filter(student=user, topic=topic).count() == 1:
        gained += _award(user, 'topic_first', topic.id, POINTS['topic_first'])
    return gained


def award_section(user, section):
    return _award(user, 'section', section.id, POINTS['section'])


def award_exam(user, book):
    return _award(user, 'exam', book.id, POINTS['exam'])


def award_review(user, review_answer_id):
    return _award(user, 'review', review_answer_id, POINTS['review'])


def total_xp(user):
    return XPEvent.objects.filter(user=user).aggregate(s=Sum('points'))['s'] or 0


def level_info(xp):
    level = xp // XP_PER_LEVEL + 1
    return {
        'level': level,
        'title': LEVEL_TITLES[min(level - 1, len(LEVEL_TITLES) - 1)],
        'xp_in_level': xp % XP_PER_LEVEL,
        'xp_for_next': XP_PER_LEVEL,
    }


def _active_dates(user):
    return {
        timezone.localtime(dt).date()
        for dt in TestAttempt.objects.filter(student=user).values_list('created_at', flat=True)
    }


def streak_info(user):
    dates = _active_dates(user)
    today = timezone.localdate()
    # Joriy ketma-ketlik: bugun yoki kecha faol bo'lgan bo'lsa davom etadi.
    cur = 0
    day = today if today in dates else today - timedelta(days=1)
    while day in dates:
        cur += 1
        day -= timedelta(days=1)
    best, run, prev = 0, 0, None
    for d in sorted(dates):
        run = run + 1 if prev and d - prev == timedelta(days=1) else 1
        best = max(best, run)
        prev = d
    return {'current': cur, 'best': best, 'active_today': today in dates}


def badges(user):
    topics_done = TopicCompletion.objects.filter(student=user).count()
    sections_done = SectionCompletion.objects.filter(student=user).count()
    certs = Certificate.objects.filter(student=user).count()
    perfect_first = XPEvent.objects.filter(user=user, kind='topic_first').count()
    best_streak = streak_info(user)['best']
    spec = [
        ('first_step', 'Birinchi qadam', "Birinchi mavzu testini topshiring", 'footprints', topics_done >= 1),
        ('five_topics', 'Faol o\'quvchi', '5 ta mavzuni o\'zlashtiring', 'book-open', topics_done >= 5),
        ('twenty_topics', 'Bilim izlovchi', '20 ta mavzuni o\'zlashtiring', 'library', topics_done >= 20),
        ('perfect', 'Mukammal', "5 ta testni birinchi urinishda 100% topshiring", 'target', perfect_first >= 5),
        ('section', "Bo'lim ustasi", "Birinchi bo'lim testini topshiring", 'flag', sections_done >= 1),
        ('streak3', '3 kunlik ketma-ketlik', "3 kun ketma-ket o'qing", 'flame', best_streak >= 3),
        ('streak7', 'Haftalik shijoat', "7 kun ketma-ket o'qing", 'zap', best_streak >= 7),
        ('graduate', 'Bitiruvchi', "Kursni tugatib, sertifikat oling", 'award', certs >= 1),
    ]
    return [
        {'key': k, 'title': t, 'description': d, 'icon': i, 'earned': bool(e)}
        for k, t, d, i, e in spec
    ]


def profile(user):
    xp = total_xp(user)
    attempts = TestAttempt.objects.filter(student=user)
    agg = attempts.aggregate(n=Count('id'))
    passed = attempts.filter(passed=True).count()
    return {
        'xp': xp,
        **level_info(xp),
        'streak': streak_info(user),
        'badges': badges(user),
        'stats': {
            'topics_done': TopicCompletion.objects.filter(student=user).count(),
            'sections_done': SectionCompletion.objects.filter(student=user).count(),
            'certificates': Certificate.objects.filter(student=user).count(),
            'attempts': agg['n'],
            'passed_attempts': passed,
        },
    }
