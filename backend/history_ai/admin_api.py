"""Boshqaruv paneli uchun REST API (faqat is_staff — IsTeacher).

Django'ning tayyor `/admin/` interfeysi bilan bir xil ma'lumot va amallarni
frontend (React) ilovaning o'zidan, alohida login/manzilga o'tmasdan
foydalanish uchun: statistika, talabalar nazorati va fan/kitob/bo'lim/mavzu/
dars/test kontentini yaratish-tahrirlash-o'chirish.
"""
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import serializers as drf_serializers
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import STATUS_DONE, Book, GeneratedAsset, Lesson, Section, Subject, Topic
from .permissions import IsTeacher
from .serializers import BookSerializer, SubjectSerializer
from .services import gamification
from .services.admin_stats import (
    platform_overview, student_activity_history, student_completed_topics, students_report,
)
from .services.book_import import _check_test_question

User = get_user_model()


class AdminStatsView(APIView):
    permission_classes = [IsTeacher]

    def get(self, request):
        return Response(platform_overview())


class AdminStudentSerializer(drf_serializers.Serializer):
    id = drf_serializers.IntegerField()
    username = drf_serializers.CharField()
    first_name = drf_serializers.CharField()
    email = drf_serializers.EmailField(allow_blank=True)
    is_active = drf_serializers.BooleanField()
    is_staff = drf_serializers.BooleanField()
    date_joined = drf_serializers.DateTimeField()
    xp = drf_serializers.IntegerField()
    topics_done = drf_serializers.IntegerField()
    certs_count = drf_serializers.IntegerField()
    total_seconds = drf_serializers.IntegerField()
    last_activity = drf_serializers.DateField(allow_null=True)


class AdminStudentListView(APIView):
    permission_classes = [IsTeacher]

    def get(self, request):
        qs = students_report(request.query_params.get('q', '').strip())
        return Response(AdminStudentSerializer(qs, many=True).data)


class AdminStudentDetailView(APIView):
    permission_classes = [IsTeacher]

    def get(self, request, user_id):
        student = get_object_or_404(User, pk=user_id)
        return Response({
            'id': student.id, 'username': student.username, 'first_name': student.first_name,
            'email': student.email, 'is_active': student.is_active, 'is_staff': student.is_staff,
            'date_joined': student.date_joined,
            'profile': gamification.profile(student),
            'activity': student_activity_history(student),
            'completed_topics': student_completed_topics(student),
            'certificates': list(
                student.certificates.select_related('book')
                .values('book__title', 'code', 'issued_at').order_by('-issued_at')
            ),
        })


class AdminStudentActionView(APIView):
    """Talabani bloklash/faollashtirish, admin (is_staff) huquqi berish/olib qo'yish."""

    permission_classes = [IsTeacher]
    VALID_ACTIONS = {'activate', 'deactivate', 'grant_staff', 'revoke_staff'}

    def post(self, request, user_id):
        action = request.data.get('action')
        if action not in self.VALID_ACTIONS:
            raise ValidationError({'action': f"Noto'g'ri amal. Mumkin: {', '.join(sorted(self.VALID_ACTIONS))}"})
        user = get_object_or_404(User, pk=user_id)
        if user.pk == request.user.pk:
            raise ValidationError({'detail': "O'zingizga nisbatan bu amalni bajara olmaysiz."})
        if action == 'activate':
            user.is_active = True
        elif action == 'deactivate':
            user.is_active = False
        elif action == 'grant_staff':
            user.is_staff = True
        elif action == 'revoke_staff':
            user.is_staff = False
        user.save(update_fields=['is_active', 'is_staff'])
        return Response({'id': user.id, 'is_active': user.is_active, 'is_staff': user.is_staff})


# ---- Kontent: fan / kitob / bo'lim / mavzu ----

class AdminSubjectListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsTeacher]
    serializer_class = SubjectSerializer
    queryset = Subject.objects.annotate(book_count=Count('books')).order_by('order', 'id')


class AdminSubjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsTeacher]
    serializer_class = SubjectSerializer
    queryset = Subject.objects.annotate(book_count=Count('books'))


class AdminBookListView(generics.ListAPIView):
    permission_classes = [IsTeacher]
    serializer_class = BookSerializer
    queryset = Book.objects.select_related('subject').order_by('-created_at')


class AdminBookDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsTeacher]
    serializer_class = BookSerializer
    queryset = Book.objects.all()


class AdminSectionSerializer(drf_serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['id', 'book', 'key', 'title', 'order']
        read_only_fields = ['book']


class AdminSectionListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsTeacher]
    serializer_class = AdminSectionSerializer

    def get_queryset(self):
        return Section.objects.filter(book_id=self.kwargs['book_id']).order_by('order')

    def perform_create(self, serializer):
        serializer.save(book_id=self.kwargs['book_id'])


class AdminSectionDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsTeacher]
    serializer_class = AdminSectionSerializer
    queryset = Section.objects.all()


class AdminTopicSerializer(drf_serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'book', 'section', 'key', 'title', 'start_page', 'end_page', 'order']
        read_only_fields = ['book', 'section']


class AdminTopicListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsTeacher]
    serializer_class = AdminTopicSerializer

    def get_queryset(self):
        return Topic.objects.filter(section_id=self.kwargs['section_id']).order_by('order')

    def perform_create(self, serializer):
        section = get_object_or_404(Section, pk=self.kwargs['section_id'])
        serializer.save(section=section, book=section.book)


class AdminTopicDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsTeacher]
    serializer_class = AdminTopicSerializer
    queryset = Topic.objects.all()


# ---- Mavzu darsi (lesson_plan) va mavzu testi tahriri ----

class AdminLessonBlockSerializer(drf_serializers.Serializer):
    heading = drf_serializers.CharField(required=False, allow_blank=True, default='')
    text = drf_serializers.CharField(allow_blank=False)
    pages = drf_serializers.ListField(child=drf_serializers.IntegerField(), required=False, default=list)


class AdminKeyFactSerializer(drf_serializers.Serializer):
    fact = drf_serializers.CharField(allow_blank=False)
    page = drf_serializers.IntegerField(required=False, allow_null=True, default=None)


class AdminLessonPlanSerializer(drf_serializers.Serializer):
    goals = drf_serializers.ListField(child=drf_serializers.CharField(), required=False, default=list)
    blocks = AdminLessonBlockSerializer(many=True)
    key_facts = AdminKeyFactSerializer(many=True, required=False, default=list)
    summary = drf_serializers.CharField(required=False, allow_blank=True, default='')

    def validate_blocks(self, value):
        if not value:
            raise drf_serializers.ValidationError("Kamida bitta blok (matn) kerak")
        return value


class AdminTopicLessonView(APIView):
    """Mavzu dars rejasini ko'rish/tahrirlash (frontend ichidan, qo'lda - AI'siz)."""

    permission_classes = [IsTeacher]

    def get(self, request, topic_id):
        topic = get_object_or_404(Topic, pk=topic_id)
        lesson = getattr(topic, 'lesson', None)
        if not lesson:
            return Response(None)
        return Response({'lesson_plan': lesson.lesson_plan, 'quiz': lesson.quiz, 'status': lesson.status})

    def put(self, request, topic_id):
        topic = get_object_or_404(Topic, pk=topic_id)
        serializer = AdminLessonPlanSerializer(data=request.data.get('lesson_plan') or {})
        serializer.is_valid(raise_exception=True)
        lesson, _ = Lesson.objects.update_or_create(
            topic=topic,
            defaults={
                'created_by': request.user, 'status': STATUS_DONE, 'ai_provider': 'manual', 'error_message': '',
                'lesson_plan': serializer.validated_data,
            },
        )
        return Response({'lesson_plan': lesson.lesson_plan, 'quiz': lesson.quiz, 'status': lesson.status})


class AdminTopicTestView(APIView):
    """Mavzu "Mavzu testi" savollarini ko'rish/tahrirlash (frontend ichidan, qo'lda - AI'siz)."""

    permission_classes = [IsTeacher]

    def get(self, request, topic_id):
        asset = GeneratedAsset.objects.filter(topic_id=topic_id, kind=GeneratedAsset.KIND_TOPIC_TEST).first()
        return Response(asset.data if asset else None)

    def put(self, request, topic_id):
        topic = get_object_or_404(Topic, pk=topic_id)
        questions = request.data.get('questions')
        if not isinstance(questions, list) or not questions:
            raise ValidationError({'questions': "Kamida bitta savol kerak"})
        errors = []
        for i, q in enumerate(questions):
            _check_test_question(q, f"savol[{i}]", errors)
        if errors:
            raise ValidationError({'questions': errors})
        asset, _ = GeneratedAsset.objects.update_or_create(
            topic=topic, kind=GeneratedAsset.KIND_TOPIC_TEST,
            defaults={
                'created_by': request.user, 'status': STATUS_DONE, 'ai_provider': 'manual', 'error_message': '',
                'data': {'questions': questions},
            },
        )
        return Response(asset.data)
