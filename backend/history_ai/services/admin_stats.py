"""Admin panel uchun butun platforma statistikasi (umumiy nazorat sahifasi)."""
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db.models import Count
from django.utils import timezone

from ..models import Book, Certificate, DailyActivity, ReviewAnswer, Subject, TestAttempt, TopicCompletion


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
