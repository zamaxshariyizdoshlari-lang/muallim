from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Book, Lesson, Page, Topic
from .serializers import BookSerializer, LessonSerializer, TopicSerializer
from .services.pdf_extractor import NoTextLayerError, extract_pages
from .services.topic_detector import detect_topics
from .tasks import start_lesson_generation


class BookUploadView(APIView):
    """PDF yuklash: betlarga ajratib saqlaydi va mavzularni aniqlaydi."""

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


class LessonCreateView(APIView):
    """Tanlangan mavzu uchun dars rejasi + test yaratishni boshlaydi (fon vazifa)."""

    def post(self, request):
        topic_id = request.data.get('topic')
        if not topic_id:
            raise ValidationError({'topic': 'topic id talab qilinadi'})

        try:
            topic = Topic.objects.get(id=topic_id)
        except Topic.DoesNotExist:
            raise ValidationError({'topic': 'Mavzu topilmadi'})

        lesson = Lesson.objects.create(topic=topic, created_by=request.user)
        start_lesson_generation(lesson.id)

        return Response(LessonSerializer(lesson).data, status=status.HTTP_202_ACCEPTED)


class LessonDetailView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
