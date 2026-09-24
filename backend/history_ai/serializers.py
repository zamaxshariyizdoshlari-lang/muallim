from rest_framework import serializers

from .models import Book, Lesson, Topic


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'file', 'has_text_layer', 'created_at']
        read_only_fields = ['id', 'has_text_layer', 'created_at']


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'book', 'title', 'start_page', 'end_page', 'order']
        read_only_fields = ['id']


class LessonSerializer(serializers.ModelSerializer):
    topic_title = serializers.CharField(source='topic.title', read_only=True)

    class Meta:
        model = Lesson
        fields = [
            'id', 'topic', 'topic_title', 'status', 'ai_provider',
            'lesson_plan', 'quiz', 'error_message', 'created_at', 'updated_at',
        ]
        read_only_fields = [
            'id', 'topic_title', 'status', 'ai_provider',
            'lesson_plan', 'quiz', 'error_message', 'created_at', 'updated_at',
        ]
