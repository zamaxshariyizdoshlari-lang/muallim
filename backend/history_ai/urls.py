from django.urls import path

from . import views

app_name = 'history_ai'

urlpatterns = [
    path('me/', views.MeView.as_view(), name='me'),
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
    path('books/<int:book_id>/search/', views.BookSearchView.as_view(), name='book-search'),
    path('books/<int:book_id>/exam/', views.BookExamByBookView.as_view(), name='book-exam'),
    path('books/<int:book_id>/exam/create/', views.BookExamCreateView.as_view(), name='book-exam-create'),
    path('books/<int:book_id>/exam/submit/', views.BookExamSubmitView.as_view(), name='book-exam-submit'),
    path('books/<int:book_id>/certificate/', views.CertificateDownloadView.as_view(), name='certificate'),
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
