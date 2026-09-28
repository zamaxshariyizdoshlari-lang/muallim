"""ball, daraja, kunlik ketma-ketlik (streak) va nishonlar.

ball jurnali (XPEvent) bir marta beriladi (user+kind+ref unikal), shuning uchun testni qayta
topshirish XPni ko'paytirmaydi. Streak va nishonlar mavjud ma'lumotlardan hisoblanadi.
"""
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.db.models import Count, Sum
from django.utils import timezone

from ..models import (
    Certificate, ReviewAnswer, SectionCompletion, TestAttempt, TopicCompletion, UserSettings, XPEvent,
)

POINTS = {
    'topic': 50, 'topic_first': 20, 'topic_perfect': 15,
    'section': 150, 'section_perfect': 30, 'exam': 300, 'review': 5,
}
XP_PER_LEVEL = 200

LEVEL_TITLES = ['Yangi boshlovchi', 'Izlanuvchi', 'Bilimdon', 'Donishmand', 'Alloma', 'Ustoz']


def _award(user, kind, ref_id, points):
    _, created = XPEvent.objects.get_or_create(
        user=user, kind=kind, ref_id=ref_id, defaults={'points': points}
    )
    return points if created else 0


def award_topic(user, topic, perfect=False):
    """Mavzu testi o'tilganda (kamida 80%): asosiy ball + birinchi urinishda bo'lsa va 100% uchun bonus."""
    gained = _award(user, 'topic', topic.id, POINTS['topic'])
    if gained and TestAttempt.objects.filter(student=user, topic=topic).count() == 1:
        gained += _award(user, 'topic_first', topic.id, POINTS['topic_first'])
    if perfect:
        gained += _award(user, 'topic_perfect', topic.id, POINTS['topic_perfect'])
    return gained


def award_section(user, section, perfect=False):
    gained = _award(user, 'section', section.id, POINTS['section'])
    if perfect:
        gained += _award(user, 'section_perfect', section.id, POINTS['section_perfect'])
    return gained


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
    """Faol kunlar: test topshirilgan yoki takrorlashda javob berilgan kunlar."""
    stamps = list(TestAttempt.objects.filter(student=user).values_list('created_at', flat=True))
    stamps += list(ReviewAnswer.objects.filter(user=user).values_list('created_at', flat=True))
    return {timezone.localtime(dt).date() for dt in stamps}


FREEZE_EVERY = 7   # har 7 faol kunda 1 ta "muzlatish" (kunni o'tkazib yuborishni kechiradi)
FREEZE_MAX = 2


def streak_info(user):
    """Ketma-ketlik. Har 7 faol kun uchun 1 ta muzlatish (maks. 2) beriladi: u bitta o'tkazilgan kunni
    kechiradi. Bugun hali tugamagani uchun bugungi faolsizlik ketma-ketlikni uzmaydi."""
    dates = _active_dates(user)
    today = timezone.localdate()
    if not dates:
        return {'current': 0, 'best': 0, 'active_today': False, 'freezes': 0}
    run = best = streak_days = freezes = 0
    day = min(dates)
    while day <= today:
        if day in dates:
            run += 1
            streak_days += 1
            best = max(best, run)
            if streak_days % FREEZE_EVERY == 0:
                freezes = min(FREEZE_MAX, freezes + 1)
        elif day != today:
            if freezes > 0:
                freezes -= 1
            else:
                run = 0
                streak_days = 0
        day += timedelta(days=1)
    return {'current': run, 'best': best, 'active_today': today in dates, 'freezes': freezes}


def get_settings(user):
    obj, _ = UserSettings.objects.get_or_create(user=user)
    return obj


def today_xp(user):
    start = timezone.localtime().replace(hour=0, minute=0, second=0, microsecond=0)
    return XPEvent.objects.filter(user=user, created_at__gte=start).aggregate(s=Sum('points'))['s'] or 0


def daily_info(user):
    goal = get_settings(user).daily_goal
    earned = today_xp(user)
    return {'goal': goal, 'today': earned, 'met': earned >= goal}


def week_start():
    today = timezone.localdate()
    monday = today - timedelta(days=today.weekday())
    return timezone.make_aware(datetime.combine(monday, datetime.min.time()))


LEAGUES = [
    {'key': 'bronze', 'title': 'Bronza', 'icon': 'award', 'min_xp': 0},
    {'key': 'silver', 'title': 'Kumush', 'icon': 'medal', 'min_xp': 500},
    {'key': 'gold', 'title': 'Oltin', 'icon': 'trophy', 'min_xp': 1500},
    {'key': 'platinum', 'title': 'Platina', 'icon': 'gem', 'min_xp': 3500},
    {'key': 'diamond', 'title': 'Olmos', 'icon': 'diamond', 'min_xp': 7000},
]


def league_for_xp(xp):
    current = LEAGUES[0]
    for league in LEAGUES:
        if xp >= league['min_xp']:
            current = league
    return current


def league_info(user):
    xp = total_xp(user)
    idx = next(i for i, l in enumerate(LEAGUES) if l['key'] == league_for_xp(xp)['key'])
    nxt = LEAGUES[idx + 1] if idx + 1 < len(LEAGUES) else None
    league = LEAGUES[idx]
    return {
        'key': league['key'], 'title': league['title'], 'icon': league['icon'],
        'next_title': nxt['title'] if nxt else None,
        'xp_to_next': (nxt['min_xp'] - xp) if nxt else 0,
    }


def _leaderboard_rows(user, user_ids, limit):
    hidden = UserSettings.objects.filter(show_in_leaderboard=False).values_list('user_id', flat=True)
    rows = list(
        XPEvent.objects.filter(created_at__gte=week_start(), user_id__in=user_ids).exclude(user_id__in=hidden)
        .values('user_id').annotate(points=Sum('points')).order_by('-points', 'user_id')
    )
    users = {u.id: u for u in get_user_model().objects.filter(id__in=[r['user_id'] for r in rows[:limit]])}
    top = [
        {
            'rank': i + 1, 'points': r['points'], 'me': r['user_id'] == user.id,
            'name': (users[r['user_id']].first_name or users[r['user_id']].username),
        }
        for i, r in enumerate(rows[:limit])
    ]
    me = next(
        ({'rank': i + 1, 'points': r['points']} for i, r in enumerate(rows) if r['user_id'] == user.id), None
    )
    return {'top': top, 'me': me, 'opted_in': get_settings(user).show_in_leaderboard, 'participants': len(rows)}


def leaderboard(user, limit=10):
    """Shu haftalik (dushanbadan) ball bo'yicha reyting, faqat foydalanuvchi bilan bir xil
    ligadagilar orasida (umumiy XP bo'yicha - bronza/kumush/oltin/platina/olmos). Shu bilan
    yangi boshlovchi doim eng ko'p ballli eskilarga emas, o'z darajasidagilarga qaraydi."""
    totals = dict(XPEvent.objects.values('user_id').annotate(t=Sum('points')).values_list('user_id', 't'))
    my_league = league_for_xp(totals.get(user.id, 0))['key']
    peer_ids = [uid for uid, xp in totals.items() if league_for_xp(xp)['key'] == my_league]
    if user.id not in peer_ids:
        peer_ids.append(user.id)
    result = _leaderboard_rows(user, peer_ids, limit)
    result['league'] = league_info(user)
    return result


def badges(user):
    topics_done = TopicCompletion.objects.filter(student=user).count()
    sections_done = SectionCompletion.objects.filter(student=user).count()
    certs = Certificate.objects.filter(student=user).count()
    perfect_count = XPEvent.objects.filter(user=user, kind__in=['topic_perfect', 'section_perfect']).count()
    best_streak = streak_info(user)['best']
    spec = [
        ('first_step', 'Birinchi qadam', "Birinchi mavzu testini topshiring", 'footprints', topics_done >= 1),
        ('five_topics', 'Faol o\'rganuvchi', '5 ta mavzuni o\'zlashtiring', 'book-open', topics_done >= 5),
        ('twenty_topics', 'Bilim izlovchi', '20 ta mavzuni o\'zlashtiring', 'library', topics_done >= 20),
        ('perfect', 'Mukammal', "5 ta testni 100% (xatosiz) topshiring", 'target', perfect_count >= 5),
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
        'league': league_info(user),
        'streak': streak_info(user),
        'daily': daily_info(user),
        'badges': badges(user),
        'stats': {
            'topics_done': TopicCompletion.objects.filter(student=user).count(),
            'sections_done': SectionCompletion.objects.filter(student=user).count(),
            'certificates': Certificate.objects.filter(student=user).count(),
            'attempts': agg['n'],
            'passed_attempts': passed,
        },
    }
