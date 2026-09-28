import random

from rest_framework import serializers

from .models import Book, BookExam, GeneratedAsset, Lesson, SectionExam, Subject, Topic


class SubjectSerializer(serializers.ModelSerializer):
    book_count = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Subject
        fields = ['id', 'slug', 'title', 'description', 'icon', 'order', 'book_count']


class BookSerializer(serializers.ModelSerializer):
    subject_slug = serializers.CharField(source='subject.slug', read_only=True, default=None)

    class Meta:
        model = Book
        fields = ['id', 'title', 'description', 'subject', 'subject_slug', 'file', 'has_text_layer', 'created_at']
        read_only_fields = ['id', 'has_text_layer', 'created_at']


def hide_answers(data, request):
    """Rasmiy test savollaridan to'g'ri javobni talabadan yashiradi (o'qituvchi ko'radi).

    Variantlar tartibi har safar aralashtiriladi: shu bilan talaba javobni "pozitsiya bo'yicha"
    yodlab, qayta urinishda o'ylamasdan bosib qo'ya olmaydi - lekin to'g'ri javobning o'zini
    (matnini) baholashdan keyin ko'rishi mumkin, chunki bu haqiqiy o'rganishga yordam beradi.
    """
    user = getattr(request, 'user', None)
    if data and not (user and user.is_staff):
        questions = []
        for q in data.get('questions', []):
            options = list(q.get('options', []))
            random.shuffle(options)
            questions.append({**{k: v for k, v in q.items() if k != 'correct_index'}, 'options': options})
        data = {**data, 'questions': questions}
    return data


class TopicSerializer(serializers.ModelSerializer):
    unlocked = serializers.SerializerMethodField()
    completed = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = ['id', 'book', 'section', 'key', 'title', 'start_page', 'end_page', 'order', 'unlocked', 'completed']
        read_only_fields = ['id']

    def _state(self, obj):
        states = self.context.get('topic_states')
        return (states or {}).get(obj.id, {'unlocked': True, 'completed': False})

    def get_unlocked(self, obj):
        return self._state(obj)['unlocked']

    def get_completed(self, obj):
        return self._state(obj)['completed']


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


class GeneratedAssetSerializer(serializers.ModelSerializer):
    topic_title = serializers.CharField(source='topic.title', read_only=True)

    class Meta:
        model = GeneratedAsset
        fields = [
            'id', 'topic', 'topic_title', 'kind', 'status', 'ai_provider',
            'data', 'error_message', 'created_at', 'updated_at',
        ]
        read_only_fields = [
            'id', 'topic_title', 'status', 'ai_provider',
            'data', 'error_message', 'created_at', 'updated_at',
        ]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.kind == GeneratedAsset.KIND_TOPIC_TEST:
            rep['data'] = hide_answers(rep['data'], self.context.get('request'))
        return rep


class SectionExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionExam
        fields = ['id', 'section', 'data']
        read_only_fields = fields

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['status'] = 'done'
        rep['data'] = hide_answers(rep['data'], self.context.get('request'))
        return rep


class BookExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookExam
        fields = ['id', 'book', 'status', 'data', 'error_message', 'created_at', 'updated_at']
        read_only_fields = fields

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['data'] = hide_answers(rep['data'], self.context.get('request'))
        return rep
