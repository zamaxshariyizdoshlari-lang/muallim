"""Admin panel uchun butun platforma statistikasi (umumiy nazorat sahifasi)."""
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db.models import Count, Max, Sum
from django.db.models.functions import Coalesce
from django.utils import timezone

from ..models import (
    Book, Certificate, DailyActivity, ReviewAnswer, Subject, TestAttempt, TopicCompletion,
)


def platform_overview():
    User = get_user_model()
    today_start = timezone.localtime().replace(hour=0, minute=0, second=0, microsecond=0)
    week_ago = timezone.now() - timedelta(days=7)

    students = User.objects.filter(is_staff=False)
    active_today = set(
        TestAttempt.objects.filter(created_at__gte=today_start).values_list('student_id', flat=True)
    ) | set(
        ReviewAnswer.objects.filter(created_at__gte=today_start).values_list('user_id', flat=True)
    )

    popular = (
        TopicCompletion.objects.values('topic__book__title')
        .annotate(n=Count('id')).order_by('-n').first()
    )

    today = timezone.localdate()
    daily_activity_today = [
        {'username': row['user__username'], 'seconds': row['seconds_active'], 'minutes': row['seconds_active'] // 60}
        for row in DailyActivity.objects.filter(date=today)
        .values('user__username', 'seconds_active').order_by('-seconds_active')[:15]
    ]

    return {
        'daily_activity_today': daily_activity_today,
        'students_total': students.count(),
        'students_active_today': len(active_today),
        'new_registrations_7d': students.filter(date_joined__gte=week_ago).count(),
        'subjects_total': Subject.objects.count(),
        'books_total': Book.objects.count(),
        'certificates_total': Certificate.objects.count(),
        'test_attempts_total': TestAttempt.objects.count(),
        'most_popular_book': popular['topic__book__title'] if popular else None,
    }


def students_report(search=''):
    """Har bir talaba uchun: jami vaqt, oxirgi faollik, o'zlashtirgan mavzular, ball — bitta jadvalda.

    "Platforma nazorati" uchun asosiy hisobot: kimlar foydalanyapti, qancha muddat, qanday natija bilan.
    """
    User = get_user_model()
    qs = User.objects.filter(is_staff=False).annotate(
        total_seconds=Coalesce(Sum('daily_activity__seconds_active'), 0),
        last_activity=Max('daily_activity__date'),
        topics_done=Count('topic_completions', distinct=True),
        certs_count=Count('certificates', distinct=True),
        xp=Coalesce(Sum('xp_events__points'), 0),
    )
    if search:
        qs = qs.filter(username__icontains=search) | qs.filter(first_name__icontains=search) | qs.filter(
            email__icontains=search
        )
    return qs.order_by('-last_activity', '-xp')


def student_activity_history(user, days=30):
    """Oxirgi N kunlik faollik (kunlik daqiqa), eng eskisi oldin (grafik uchun)."""
    since = timezone.localdate() - timedelta(days=days - 1)
    rows = {
        row['date']: row['seconds_active']
        for row in DailyActivity.objects.filter(user=user, date__gte=since).values('date', 'seconds_active')
    }
    today = timezone.localdate()
    return [
        {'date': today - timedelta(days=i), 'minutes': rows.get(today - timedelta(days=i), 0) // 60}
        for i in range(days - 1, -1, -1)
    ]


def student_completed_topics(user):
    """Talaba o'zlashtirgan mavzular ro'yxati, kurs/bo'lim va sanasi bilan (eng yangisi oldin)."""
    return list(
        TopicCompletion.objects.filter(student=user)
        .select_related('topic', 'topic__book', 'topic__section')
        .order_by('-completed_at')
        .values(
            'completed_at', 'topic__title', 'topic__book__title', 'topic__section__title',
        )
    )
