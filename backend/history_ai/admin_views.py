"""Admin panelning maxsus sahifalari (oddiy ModelAdmin bilan qilib bo'lmaydigan)."""
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render

from .services import gamification
from .services.admin_stats import (
    platform_overview, student_activity_history, student_completed_topics, students_report,
)


@staff_member_required
def dashboard_view(request):
    from django.contrib import admin

    context = {
        **admin.site.each_context(request),
        'title': 'Platforma statistikasi',
        'stats': platform_overview(),
    }
    return render(request, 'admin/statistika.html', context)


@staff_member_required
def students_report_view(request):
    from django.contrib import admin

    search = request.GET.get('q', '').strip()
    context = {
        **admin.site.each_context(request),
        'title': 'Talabalar nazorati',
        'students': students_report(search),
        'search': search,
    }
    return render(request, 'admin/talabalar.html', context)


@staff_member_required
def student_detail_view(request, user_id):
    from django.contrib import admin

    student = get_object_or_404(get_user_model(), pk=user_id, is_staff=False)
    activity = student_activity_history(student)
    context = {
        **admin.site.each_context(request),
        'title': f"Talaba: {student.first_name or student.username}",
        'student': student,
        'profile': gamification.profile(student),
        'activity': activity,
        'max_minutes': max((d['minutes'] for d in activity), default=0) or 1,
        'completed_topics': student_completed_topics(student),
        'certificates': student.certificates.select_related('book').order_by('-issued_at'),
    }
    return render(request, 'admin/talaba_detail.html', context)
