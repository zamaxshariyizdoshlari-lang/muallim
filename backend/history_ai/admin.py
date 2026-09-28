"""Admin panel: platformadagi hamma narsa ustidan nazorat (mukammal nazorat).

Django'ning tayyor, sinovdan o'tgan admin interfeysidan foydalaniladi - alohida
"admin frontend" qurishning hojati yo'q. `/admin/` manzilida faqat is_staff=True
hisoblar kira oladi; "Platforma statistikasi" havolasi bosh sahifada chiqadi.
"""
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.db.models import Count, Max, Sum
from django.urls import path, reverse
from django.utils.html import format_html

from . import admin_views
from .models import (
    Book, Certificate, DailyActivity, Friendship, GeneratedAsset, Lesson, ReviewAnswer, ReviewCard, Section,
    SectionCompletion, SectionExam, StudentGroup, Subject, TestAttempt, Topic, TopicCompletion, UserSettings,
    XPEvent,
)

admin.site.site_header = 'Muallim - boshqaruv paneli'
admin.site.site_title = 'Muallim admin'
admin.site.index_title = "Nazorat paneli"

# Statistika sahifasini standart admin URL'lariga qo'shamiz (index.html'dagi havola shunga ishora qiladi).
_original_get_urls = admin.site.get_urls


def _get_urls():
    return [
        path('statistika/', admin_views.dashboard_view, name='statistika'),
        path('talabalar/', admin_views.students_report_view, name='talabalar'),
        path('talabalar/<int:user_id>/', admin_views.student_detail_view, name='talaba-detail'),
    ] + _original_get_urls()


admin.site.get_urls = _get_urls


User = get_user_model()


@admin.action(description="Tanlanganlarni faollashtirish")
def activate_users(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.action(description="Tanlanganlarni bloklash (faolsizlantirish)")
def deactivate_users(modeladmin, request, queryset):
    queryset.exclude(pk=request.user.pk).update(is_active=False)


@admin.action(description="Admin huquqi berish (is_staff)")
def grant_staff(modeladmin, request, queryset):
    queryset.update(is_staff=True)


@admin.action(description="Admin huquqini olib qo'yish")
def revoke_staff(modeladmin, request, queryset):
    queryset.exclude(pk=request.user.pk).update(is_staff=False)


class UserAdmin(DjangoUserAdmin):
    """Standart Django foydalanuvchi admini + o'rganish faolligi ustunlari (faqat ko'rish uchun)."""

    list_display = (
        'username', 'first_name', 'email', 'is_active', 'is_staff', 'xp_column', 'topics_done_column',
        'certificates_column', 'total_time_column', 'last_activity_column', 'date_joined', 'detail_link',
    )
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    actions = [activate_users, deactivate_users, grant_staff, revoke_staff]

    def get_queryset(self, request):
        return (
            super().get_queryset(request)
            .annotate(
                _xp=Sum('xp_events__points'), _topics=Count('topic_completions', distinct=True),
                _certs=Count('certificates', distinct=True),
                _seconds=Sum('daily_activity__seconds_active'), _last_seen=Max('daily_activity__date'),
            )
        )

    @admin.display(description='Ball', ordering='_xp')
    def xp_column(self, obj):
        return obj._xp or 0

    @admin.display(description="O'zlashtirgan mavzu", ordering='_topics')
    def topics_done_column(self, obj):
        return obj._topics

    @admin.display(description='Sertifikat', ordering='_certs')
    def certificates_column(self, obj):
        return obj._certs

    @admin.display(description='Jami vaqt', ordering='_seconds')
    def total_time_column(self, obj):
        seconds = obj._seconds or 0
        hours, minutes = divmod(seconds // 60, 60)
        return f"{hours} soat {minutes} daq" if hours else f"{minutes} daq"

    @admin.display(description='Oxirgi faollik', ordering='_last_seen')
    def last_activity_column(self, obj):
        return obj._last_seen or '—'

    @admin.display(description='Batafsil')
    def detail_link(self, obj):
        if obj.is_staff:
            return '—'
        return format_html('<a href="{}">Nazorat &rarr;</a>', reverse('admin:talaba-detail', args=[obj.pk]))


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'slug')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'key', 'uploaded_by', 'topics_count', 'certificates_count', 'created_at')
    list_filter = ('subject',)
    search_fields = ('title', 'key')

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            _topics=Count('topics', distinct=True), _certs=Count('certificates', distinct=True),
        )

    @admin.display(description='Mavzular', ordering='_topics')
    def topics_count(self, obj):
        return obj._topics

    @admin.display(description='Sertifikatlar', ordering='_certs')
    def certificates_count(self, obj):
        return obj._certs


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'book', 'order')
    list_filter = ('book',)
    search_fields = ('title',)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'book', 'section', 'start_page', 'end_page', 'order')
    list_filter = ('book',)
    search_fields = ('title', 'key')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('topic', 'status', 'ai_provider', 'updated_at')
    list_filter = ('status',)
    search_fields = ('topic__title',)


@admin.register(GeneratedAsset)
class GeneratedAssetAdmin(admin.ModelAdmin):
    list_display = ('topic', 'kind', 'status', 'updated_at')
    list_filter = ('kind', 'status')
    search_fields = ('topic__title',)


@admin.register(SectionExam)
class SectionExamAdmin(admin.ModelAdmin):
    list_display = ('section', 'created_at')
    search_fields = ('section__title',)


@admin.register(TestAttempt)
class TestAttemptAdmin(admin.ModelAdmin):
    list_display = ('student', 'topic', 'section', 'book', 'score', 'total', 'passed', 'created_at')
    list_filter = ('passed', 'created_at')
    search_fields = ('student__username',)
    date_hierarchy = 'created_at'


@admin.register(TopicCompletion)
class TopicCompletionAdmin(admin.ModelAdmin):
    list_display = ('student', 'topic', 'completed_at')
    search_fields = ('student__username', 'topic__title')
    date_hierarchy = 'completed_at'


@admin.register(SectionCompletion)
class SectionCompletionAdmin(admin.ModelAdmin):
    list_display = ('student', 'section', 'completed_at')
    search_fields = ('student__username',)


@admin.action(description="Tanlangan sertifikatlarni bekor qilish (o'chirish)")
def revoke_certificates(modeladmin, request, queryset):
    for cert in queryset:
        cert.file.delete(save=False)
    queryset.delete()


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    """Berilgan sertifikatlar nazorati: soxta/xato sertifikatni bekor qilish mumkin."""

    list_display = ('student', 'book', 'code', 'issued_at')
    search_fields = ('student__username', 'book__title', 'code')
    date_hierarchy = 'issued_at'
    actions = [revoke_certificates]


@admin.register(XPEvent)
class XPEventAdmin(admin.ModelAdmin):
    list_display = ('user', 'kind', 'points', 'created_at')
    list_filter = ('kind',)
    search_fields = ('user__username',)


@admin.register(ReviewAnswer)
class ReviewAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'qkey', 'correct', 'created_at')
    list_filter = ('correct',)
    search_fields = ('user__username',)


@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('from_user__username', 'to_user__username')


@admin.register(StudentGroup)
class StudentGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher', 'created_at')
    search_fields = ('name', 'teacher__username')
    filter_horizontal = ('students',)


@admin.register(ReviewCard)
class ReviewCardAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'qkey', 'interval_idx', 'due_date')
    list_filter = ('interval_idx',)
    search_fields = ('user__username',)


@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'daily_goal', 'show_in_leaderboard')
    search_fields = ('user__username',)


@admin.register(DailyActivity)
class DailyActivityAdmin(admin.ModelAdmin):
    """Har bir foydalanuvchi qaysi kuni qancha vaqt platformada bo'lganining kunlik jadvali."""

    list_display = ('user', 'date', 'duration_column')
    list_filter = ('date',)
    search_fields = ('user__username',)
    date_hierarchy = 'date'
    ordering = ('-date', 'user')

    @admin.display(description="Davomiylik", ordering='seconds_active')
    def duration_column(self, obj):
        minutes, seconds = divmod(obj.seconds_active, 60)
        hours, minutes = divmod(minutes, 60)
        if hours:
            return f"{hours} soat {minutes} daq"
        return f"{minutes} daq {seconds} son"
