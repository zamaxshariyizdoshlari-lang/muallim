"""Admin paneli uchun chuqur tahlil: umumiy ko'rinish, kurslar voronkasi, xavf ostidagi talabalar, faollik lentasi."""
from collections import defaultdict
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db.models import Avg, Count, Sum
from django.db.models.functions import TruncDate
from django.utils import timezone

from ..models import (
    Book, Certificate, DailyActivity, TestAttempt, Topic, TopicCompletion,
)

INACTIVE_DAYS = 7      # shuncha kun faolsiz bo'lib, kursni boshlab qo'ygan talaba "xavf ostida"
STUCK_FAILS = 3        # bitta mavzuni shuncha marta o'ta olmagan talaba "qotib qolgan"


def _series(days, rows):
    """{sana: qiymat} -> oxirgi `days` kun uchun [{'date','value'}], bo'sh kunlar 0."""
    today = timezone.localdate()
    return [
        {'date': (today - timedelta(days=i)).isoformat(), 'value': rows.get(today - timedelta(days=i), 0)}
        for i in range(days - 1, -1, -1)
    ]


def _delta(cur, prev):
    if not prev:
        return None if not cur else 100
    return round((cur - prev) / prev * 100)


def book_summaries():
    """Har bir kurs bo'yicha: nechta talaba boshlagan, o'rtacha progress, sertifikat, o'tish foizi."""
    out = []
    for book in Book.objects.select_related('subject').order_by('id'):
        topics_total = Topic.objects.filter(book=book).count()
        attempts = TestAttempt.objects.filter(topic__book=book, student__is_staff=False)
        started = set(attempts.values_list('student_id', flat=True))
        done = TopicCompletion.objects.filter(topic__book=book, student__is_staff=False).count()
        n_att = attempts.count()
        passed = attempts.filter(passed=True).count()
        out.append({
            'id': book.id, 'title': book.title, 'subject': book.subject.title if book.subject_id else '',
            'topics_total': topics_total, 'students': len(started), 'completions': done,
            'avg_progress': round(done / (len(started) * topics_total) * 100) if started and topics_total else 0,
            'certificates': Certificate.objects.filter(book=book).count(),
            'attempts': n_att, 'pass_rate': round(passed / n_att * 100) if n_att else None,
        })
    return out


def at_risk_students(limit=8):
    """Faolligi pasaygan yoki bir mavzuda qotib qolgan talabalar."""
    User = get_user_model()
    today = timezone.localdate()
    cutoff = today - timedelta(days=INACTIVE_DAYS)
    students = {u.id: u for u in User.objects.filter(is_staff=False, is_active=True)}
    last_seen = {}
    for sid, d in DailyActivity.objects.values_list('user_id', 'date'):
        if sid not in last_seen or d > last_seen[sid]:
            last_seen[sid] = d
    for sid, at in TestAttempt.objects.values_list('student_id', 'created_at'):
        d = timezone.localtime(at).date()
        if sid not in last_seen or d > last_seen[sid]:
            last_seen[sid] = d
    done = dict(
        TopicCompletion.objects.values('student_id').annotate(n=Count('id')).values_list('student_id', 'n')
    )
    rows = []
    for sid, u in students.items():
        n_done = done.get(sid, 0)
        seen = last_seen.get(sid)
        if n_done and seen and seen < cutoff:
            rows.append({
                'id': sid, 'username': u.username, 'name': u.first_name, 'reason': 'inactive',
                'detail': f"{(today - seen).days} kun faol emas, {n_done} ta mavzu tugatgan",
                'days': (today - seen).days,
            })
    passed = set(TopicCompletion.objects.values_list('student_id', 'topic_id'))
    fails = defaultdict(int)
    for sid, tid in TestAttempt.objects.filter(
        topic__isnull=False, passed=False, student__is_staff=False
    ).values_list('student_id', 'topic_id'):
        fails[(sid, tid)] += 1
    titles = {t.id: t.title for t in Topic.objects.all()}
    for (sid, tid), n in fails.items():
        if n >= STUCK_FAILS and (sid, tid) not in passed and sid in students:
            u = students[sid]
            rows.append({
                'id': sid, 'username': u.username, 'name': u.first_name, 'reason': 'stuck',
                'detail': f"{n} marta o'ta olmagan: {titles.get(tid, '')[:60]}", 'days': 0,
            })
    rows.sort(key=lambda r: (r['reason'] != 'stuck', -r['days']))
    return rows[:limit]


def activity_feed(limit=20):
    User = get_user_model()
    events = []
    for a in TestAttempt.objects.filter(student__is_staff=False).select_related('student', 'topic').order_by(
        '-created_at'
    )[:limit]:
        events.append({
            'at': a.created_at, 'kind': 'pass' if a.passed else 'fail', 'user_id': a.student_id,
            'user': a.student.first_name or a.student.username,
            'text': f"{(a.topic.title if a.topic else 'Imtihon')[:70]} - {a.score}/{a.total}",
        })
    for c in Certificate.objects.select_related('student', 'book').order_by('-id')[:limit]:
        if c.issued_at:
            events.append({
                'at': c.issued_at, 'kind': 'certificate', 'user_id': c.student_id,
                'user': c.student.first_name or c.student.username, 'text': f"Sertifikat: {c.book.title[:60]}",
            })
    for u in User.objects.filter(is_staff=False).order_by('-date_joined')[:limit]:
        events.append({
            'at': u.date_joined, 'kind': 'signup', 'user_id': u.id, 'user': u.first_name or u.username,
            'text': "Ro'yxatdan o'tdi",
        })
    events.sort(key=lambda e: e['at'], reverse=True)
    for e in events:
        e['at'] = e['at'].isoformat()
    return events[:limit]


def overview(days=30):
    User = get_user_model()
    today = timezone.localdate()
    start = today - timedelta(days=days - 1)
    students = User.objects.filter(is_staff=False)

    signups = defaultdict(int)
    for d in students.filter(date_joined__date__gte=start).annotate(d=TruncDate('date_joined')).values_list(
        'd', flat=True
    ):
        signups[d] += 1
    base = DailyActivity.objects.filter(date__gte=start, user__is_staff=False)
    active = dict(base.values('date').annotate(n=Count('user', distinct=True)).values_list('date', 'n'))
    minutes = dict(base.values('date').annotate(s=Sum('seconds_active')).values_list('date', 's'))
    att_total, att_pass = defaultdict(int), defaultdict(int)
    for at, ok in TestAttempt.objects.filter(
        created_at__date__gte=start, student__is_staff=False
    ).values_list('created_at', 'passed'):
        d = timezone.localtime(at).date()
        att_total[d] += 1
        att_pass[d] += int(ok)

    def window(rows, a, b):  # [today-a, today-b] oralig'idagi yig'indi
        return sum(v for d, v in rows.items() if today - timedelta(days=a) <= d <= today - timedelta(days=b))

    new_7, new_prev = window(signups, 6, 0), window(signups, 13, 7)
    att_7, att_prev = window(att_total, 6, 0), window(att_total, 13, 7)
    pass_7 = window(att_pass, 6, 0)
    active_users_7 = DailyActivity.objects.filter(
        date__gte=today - timedelta(days=6), user__is_staff=False
    ).values('user').distinct().count()
    active_users_prev = DailyActivity.objects.filter(
        date__gte=today - timedelta(days=13), date__lte=today - timedelta(days=7), user__is_staff=False
    ).values('user').distinct().count()
    total_students = students.count()
    minutes_7 = window(minutes, 6, 0) // 60

    return {
        'kpis': {
            'students_total': total_students,
            'new_7d': new_7, 'new_delta': _delta(new_7, new_prev),
            'active_today': active.get(today, 0),
            'active_7d': active_users_7, 'active_delta': _delta(active_users_7, active_users_prev),
            'attempts_7d': att_7, 'attempts_delta': _delta(att_7, att_prev),
            'pass_rate_7d': round(pass_7 / att_7 * 100) if att_7 else None,
            'completions_total': TopicCompletion.objects.filter(student__is_staff=False).count(),
            'certificates_total': Certificate.objects.count(),
            'avg_minutes_per_active': round(minutes_7 / active_users_7) if active_users_7 else 0,
            'engagement_7d': round(active_users_7 / total_students * 100) if total_students else 0,
        },
        'series': {
            'signups': _series(days, signups),
            'active': _series(days, active),
            'attempts': _series(days, att_total),
            'passed': _series(days, att_pass),
            'minutes': _series(days, {d: s // 60 for d, s in minutes.items()}),
        },
        'courses': book_summaries(),
        'at_risk': at_risk_students(),
        'feed': activity_feed(),
    }


def course_funnel(book):
    """Kurs mavzulari bo'yicha voronka: nechta talaba urindi, nechtasi o'tdi, qiyinlik."""
    topics = list(Topic.objects.filter(book=book).order_by('order'))
    att = (
        TestAttempt.objects.filter(topic__book=book, student__is_staff=False)
        .values('topic_id').annotate(n=Count('id'), students=Count('student', distinct=True))
    )
    by_topic = {r['topic_id']: r for r in att}
    totals = {}
    for tid, sc, tot in TestAttempt.objects.filter(topic__book=book, student__is_staff=False).values_list(
        'topic_id', 'score', 'total'
    ):
        s = totals.setdefault(tid, [0, 0])
        s[0] += sc
        s[1] += tot
    comp = dict(
        TopicCompletion.objects.filter(topic__book=book, student__is_staff=False).values('topic_id')
        .annotate(n=Count('id')).values_list('topic_id', 'n')
    )
    out = []
    for t in topics:
        r = by_topic.get(t.id)
        students = r['students'] if r else 0
        done = comp.get(t.id, 0)
        sc = totals.get(t.id)
        out.append({
            'id': t.id, 'title': t.title, 'order': t.order, 'attempts': r['n'] if r else 0, 'students': students,
            'completions': done,
            'completion_rate': round(done / students * 100) if students else None,
            'avg_score': round(sc[0] / sc[1] * 100) if sc and sc[1] else None,
            'attempts_per_student': round(r['n'] / students, 1) if r and students else None,
        })
    return out
