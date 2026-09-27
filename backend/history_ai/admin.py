"""Admin panel: platformadagi hamma narsa ustidan nazorat (mukammal nazorat).

Django'ning tayyor, sinovdan o'tgan admin interfeysidan foydalaniladi - alohida
"admin frontend" qurishning hojati yo'q. `/admin/` manzilida faqat is_staff=True
hisoblar kira oladi; "Platforma statistikasi" havolasi bosh sahifada chiqadi.
"""
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.db.models import Count, Sum
from django.urls import path

from . import admin_views
from .models import (
    Book, Certificate, GeneratedAsset, Lesson, ReviewAnswer, ReviewCard, Section, SectionCompletion,
    SectionExam, Subject, TestAttempt, Topic, TopicCompletion, UserSettings, XPEvent,
)

admin.site.site_header = 'Muallim - boshqaruv paneli'
admin.site.site_title = 'Muallim admin'
admin.site.index_title = "Nazorat paneli"

# Statistika sahifasini standart admin URL'lariga qo'shamiz (index.html'dagi havola shunga ishora qiladi).
_original_get_urls = admin.site.get_urls


def _get_urls():
    return [
        path('statistika/', admin_views.dashboard_view, name='statistika'),
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
        'certificates_column', 'date_joined', 'last_login',
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


@admin.register(ReviewCard)
class ReviewCardAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'qkey', 'interval_idx', 'due_date')
    list_filter = ('interval_idx',)
    search_fields = ('user__username',)


@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'daily_goal', 'show_in_leaderboard')
    search_fields = ('user__username',)
