from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import STATUS_PENDING, Book, GeneratedAsset, Lesson, Page, Topic
from .permissions import IsTeacher
from .serializers import BookSerializer, GeneratedAssetSerializer, LessonSerializer, TopicSerializer
from .services.pdf_extractor import NoTextLayerError, extract_pages
from .services.topic_detector import detect_topics
from .tasks import start_asset_generation, start_lesson_generation
from .throttles import AIGenerationThrottle

VALID_ASSET_KINDS = {choice[0] for choice in GeneratedAsset.KIND_CHOICES}


def _is_truthy(value):
    return str(value).lower() in ('1', 'true', 'yes')


class BookUploadView(APIView):
    """PDF yuklash: betlarga ajratib saqlaydi va mavzularni aniqlaydi. Faqat o'qituvchi."""

    permission_classes = [IsTeacher]

    def post(self, request):
        file_obj = request.FILES.get('file')
        if not file_obj:
            raise ValidationError({'file': 'PDF fayl talab qilinadi'})

        title = request.data.get('title') or file_obj.name
        book = Book.objects.create(title=title, file=file_obj, uploaded_by=request.user)

        try:
            pages = extract_pages(book.file.path)
        except NoTextLayerError as exc:
            book.has_text_layer = False
            book.save()
            return Response(
                {'book': BookSerializer(book).data, 'error': str(exc)},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        Page.objects.bulk_create([
            Page(book=book, page_number=num, text=text) for num, text in pages
        ])

        topics_data = detect_topics(pages)
        topics = Topic.objects.bulk_create([
            Topic(
                book=book,
                title=t['title'],
                start_page=t['start_page'],
                end_page=t['end_page'],
                order=i,
            )
            for i, t in enumerate(topics_data)
        ])

        return Response({
            'book': BookSerializer(book).data,
            'topics': TopicSerializer(topics, many=True).data,
        }, status=status.HTTP_201_CREATED)


class TopicListView(generics.ListAPIView):
    serializer_class = TopicSerializer

    def get_queryset(self):
        return Topic.objects.filter(book_id=self.kwargs['book_id'])


class LessonByTopicView(generics.RetrieveAPIView):
    """Mavjud lesson'ni ko'rish uchun (o'quvchilar ham). Hali yaratilmagan bo'lsa 404."""

    serializer_class = LessonSerializer

    def get_object(self):
        return get_object_or_404(Lesson, topic_id=self.kwargs['topic_id'])


class LessonCreateView(APIView):
    """Dars rejasi + test yaratish/qayta yaratishni boshlaydi. Faqat o'qituvchi.

    Mavzu uchun bitta lesson bor (get-or-create) — allaqachon mavjud bo'lsa va
    "regenerate" berilmagan bo'lsa, AI qayta chaqirilmaydi, mavjudi qaytariladi.
    """

    permission_classes = [IsTeacher]
    throttle_classes = [AIGenerationThrottle]

    def post(self, request):
        topic_id = request.data.get('topic')
        if not topic_id:
            raise ValidationError({'topic': 'topic id talab qilinadi'})

        try:
            topic = Topic.objects.get(id=topic_id)
        except Topic.DoesNotExist:
            raise ValidationError({'topic': 'Mavzu topilmadi'})

        lesson, created = Lesson.objects.get_or_create(topic=topic, defaults={'created_by': request.user})
        regenerate = _is_truthy(request.data.get('regenerate', False))

        if not created and not regenerate:
            return Response(LessonSerializer(lesson).data, status=status.HTTP_200_OK)

        if not created and lesson.status == STATUS_PENDING:
            # Generatsiya allaqachon ketmoqda - qayta ishga tushirmaymiz (poyga holatini oldini olish).
            return Response(LessonSerializer(lesson).data, status=status.HTTP_202_ACCEPTED)

        lesson.status = STATUS_PENDING
        lesson.error_message = ''
        lesson.save(update_fields=['status', 'error_message'])
        start_lesson_generation(lesson.id)
        return Response(LessonSerializer(lesson).data, status=status.HTTP_202_ACCEPTED)


class LessonDetailView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class GeneratedAssetByTopicView(generics.RetrieveAPIView):
    """Mavjud taqdimot/o'yinni ko'rish uchun (o'quvchilar ham). Hali yaratilmagan bo'lsa 404."""

    serializer_class = GeneratedAssetSerializer

    def get_object(self):
        return get_object_or_404(
            GeneratedAsset, topic_id=self.kwargs['topic_id'], kind=self.kwargs['kind']
        )


class GeneratedAssetCreateView(APIView):
    """Taqdimot/o'yin yaratish/qayta yaratishni boshlaydi. Faqat o'qituvchi.

    kind: presentation (AI, fon vazifa) | game_timeline | game_matching | game_fill_blank (qoida, darhol).
    Mavzu+kind uchun bitta yozuv bor (get-or-create) — mavjud bo'lsa va "regenerate"
    berilmagan bo'lsa, qayta yaratilmaydi.
    """

    permission_classes = [IsTeacher]
    throttle_classes = [AIGenerationThrottle]

    def post(self, request):
        topic_id = request.data.get('topic')
        kind = request.data.get('kind')

        if not topic_id:
            raise ValidationError({'topic': 'topic id talab qilinadi'})
        if kind not in VALID_ASSET_KINDS:
            raise ValidationError({'kind': f"kind quyidagilardan biri bo'lishi kerak: {sorted(VALID_ASSET_KINDS)}"})

        try:
            topic = Topic.objects.get(id=topic_id)
        except Topic.DoesNotExist:
            raise ValidationError({'topic': 'Mavzu topilmadi'})

        asset, created = GeneratedAsset.objects.get_or_create(
            topic=topic, kind=kind, defaults={'created_by': request.user}
        )
        regenerate = _is_truthy(request.data.get('regenerate', False))

        if not created and not regenerate:
            return Response(GeneratedAssetSerializer(asset).data, status=status.HTTP_200_OK)

        if not created and asset.status == STATUS_PENDING:
            # Generatsiya allaqachon ketmoqda - qayta ishga tushirmaymiz (poyga holatini oldini olish).
            return Response(GeneratedAssetSerializer(asset).data, status=status.HTTP_202_ACCEPTED)

        asset.status = STATUS_PENDING
        asset.error_message = ''
        asset.save(update_fields=['status', 'error_message'])
        start_asset_generation(asset.id)
        asset.refresh_from_db()  # qoida asosidagi turlar sinxron tugaydi - yangi holatni olish kerak
        return Response(GeneratedAssetSerializer(asset).data, status=status.HTTP_202_ACCEPTED)


class GeneratedAssetDetailView(generics.RetrieveAPIView):
    queryset = GeneratedAsset.objects.all()
    serializer_class = GeneratedAssetSerializer
