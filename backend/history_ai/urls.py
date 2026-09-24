from django.urls import path

from . import views

app_name = 'history_ai'

urlpatterns = [
    path('books/', views.BookUploadView.as_view(), name='book-upload'),
    path('books/<int:book_id>/topics/', views.TopicListView.as_view(), name='topic-list'),
    path('lessons/', views.LessonCreateView.as_view(), name='lesson-create'),
    path('lessons/<int:pk>/', views.LessonDetailView.as_view(), name='lesson-detail'),
    path('assets/', views.GeneratedAssetCreateView.as_view(), name='asset-create'),
    path('assets/<int:pk>/', views.GeneratedAssetDetailView.as_view(), name='asset-detail'),
]
