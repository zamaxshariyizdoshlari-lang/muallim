from django.urls import path

from . import admin_api, views

app_name = 'history_ai'

urlpatterns = [
    path('admin/stats/', admin_api.AdminStatsView.as_view(), name='admin-stats'),
    path('admin/students/', admin_api.AdminStudentListView.as_view(), name='admin-students'),
    path('admin/students/<int:user_id>/', admin_api.AdminStudentDetailView.as_view(), name='admin-student-detail'),
    path(
        'admin/students/<int:user_id>/action/', admin_api.AdminStudentActionView.as_view(),
        name='admin-student-action',
    ),
    path('admin/subjects/', admin_api.AdminSubjectListCreateView.as_view(), name='admin-subjects'),
    path('admin/subjects/<int:pk>/', admin_api.AdminSubjectDetailView.as_view(), name='admin-subject-detail'),
    path('admin/books/', admin_api.AdminBookListView.as_view(), name='admin-books'),
    path('admin/books/<int:pk>/', admin_api.AdminBookDetailView.as_view(), name='admin-book-detail'),
    path(
        'admin/books/<int:book_id>/sections/', admin_api.AdminSectionListCreateView.as_view(),
        name='admin-sections',
    ),
    path('admin/sections/<int:pk>/', admin_api.AdminSectionDetailView.as_view(), name='admin-section-detail'),
    path(
        'admin/sections/<int:section_id>/topics/', admin_api.AdminTopicListCreateView.as_view(),
        name='admin-topics',
    ),
    path('admin/topics/<int:pk>/', admin_api.AdminTopicDetailView.as_view(), name='admin-topic-detail'),
    path(
        'admin/topics/<int:topic_id>/lesson/', admin_api.AdminTopicLessonView.as_view(),
        name='admin-topic-lesson',
    ),
    path('admin/topics/<int:topic_id>/test/', admin_api.AdminTopicTestView.as_view(), name='admin-topic-test'),
    path('me/', views.MeView.as_view(), name='me'),
    path('heartbeat/', views.HeartbeatView.as_view(), name='heartbeat'),
    path('leaderboard/', views.LeaderboardView.as_view(), name='leaderboard'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('subjects/', views.SubjectListView.as_view(), name='subject-list'),
    path('books/import/', views.BookImportView.as_view(), name='book-import'),
    path('books/<int:book_id>/sections/', views.SectionListView.as_view(), name='section-list'),
    path('sections/<int:section_id>/exam/', views.SectionExamByIdView.as_view(), name='section-exam'),
    path('sections/<int:section_id>/exam/submit/', views.SectionExamSubmitView.as_view(), name='section-exam-submit'),
    path('books/', views.BookUploadView.as_view(), name='book-upload'),
    path('books/<int:book_id>/progress/', views.BookProgressView.as_view(), name='book-progress'),
    path('books/<int:book_id>/review/', views.ReviewListView.as_view(), name='review-list'),
    path('books/<int:book_id>/review/answer/', views.ReviewAnswerView.as_view(), name='review-answer'),
    path('books/<int:book_id>/analytics/', views.BookAnalyticsView.as_view(), name='book-analytics'),
    path('books/<int:book_id>/search/', views.BookSearchView.as_view(), name='book-search'),
    path('books/<int:book_id>/exam/', views.BookExamByBookView.as_view(), name='book-exam'),
    path('books/<int:book_id>/exam/create/', views.BookExamCreateView.as_view(), name='book-exam-create'),
    path('books/<int:book_id>/exam/submit/', views.BookExamSubmitView.as_view(), name='book-exam-submit'),
    path('books/<int:book_id>/certificate/', views.CertificateDownloadView.as_view(), name='certificate'),
    path('certificates/verify/<str:code>/', views.CertificateVerifyView.as_view(), name='certificate-verify'),
    path('topics/<int:topic_id>/test/submit/', views.TopicTestSubmitView.as_view(), name='topic-test-submit'),
    path('books/<int:book_id>/topics/', views.TopicListView.as_view(), name='topic-list'),
    path('topics/<int:topic_id>/lesson/', views.LessonByTopicView.as_view(), name='lesson-by-topic'),
    path('lessons/', views.LessonCreateView.as_view(), name='lesson-create'),
    path('lessons/<int:pk>/', views.LessonDetailView.as_view(), name='lesson-detail'),
    path(
        'topics/<int:topic_id>/assets/<str:kind>/',
        views.GeneratedAssetByTopicView.as_view(),
        name='asset-by-topic',
    ),
    path('assets/', views.GeneratedAssetCreateView.as_view(), name='asset-create'),
    path('assets/<int:pk>/', views.GeneratedAssetDetailView.as_view(), name='asset-detail'),
]
