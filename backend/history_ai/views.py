from django.core.files.base import ContentFile
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Count
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    STATUS_DONE, STATUS_FAILED, STATUS_PENDING, Book, BookExam, Certificate, GeneratedAsset,
    Lesson, Page, ReviewAnswer, Section, SectionCompletion, SectionExam, Subject, TestAttempt, Topic,
    TopicCompletion,
)
from .permissions import IsTeacher
from .progress import all_topics_completed, section_states, topic_states
from .serializers import (
    BookExamSerializer, BookSerializer, GeneratedAssetSerializer, LessonSerializer,
    SectionExamSerializer, SubjectSerializer, TopicSerializer,
)
from .services.book_exam_builder import build_book_exam
from .services.book_import import import_book_json
from .services import gamification, review as review_service
from .services.certificate import build_certificate_pdf
from .services.pdf_extractor import NoTextLayerError, extract_pages
from .services.rules.exceptions import NotEnoughDataError
from .services.topic_detector import detect_topics
from .tasks import start_asset_generation, start_lesson_generation
from .throttles import AIGenerationThrottle

VALID_ASSET_KINDS = {choice[0] for choice in GeneratedAsset.KIND_CHOICES}


def _guard_not_imported(book):
    """JSON'dan import qilingan kitob materialini AI/qoida bilan tasodifan qayta yozib yubormaslik uchun."""
    if book.key:
        raise ValidationError({'detail': "Bu kitob JSON'dan import qilingan: materialni JSON orqali yangilang."})


def _is_truthy(value):
    return str(value).lower() in ('1', 'true', 'yes')


class BookUploadView(APIView):
    """PDF yuklash: betlarga ajratib saqlaydi va mavzularni aniqlaydi. Faqat o'qituvchi."""

    def get_permissions(self):
        # Kitoblar ro'yxatini hamma ko'ra oladi; yuklash faqat o'qituvchiga.
        return [IsAuthenticated()] if self.request.method == 'GET' else [IsTeacher()]

    def get(self, request):
        books = Book.objects.select_related('subject').order_by('-created_at')
        slug = request.query_params.get('subject')
        if slug:
            books = books.filter(subject__slug=slug)
        return Response(BookSerializer(books, many=True).data)

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


class MeView(APIView):
    def get(self, request):
        u = request.user
        return Response({
            'username': u.username,
            'first_name': u.first_name,
            'is_staff': u.is_staff,
            'date_joined': u.date_joined,
        })


class ProfileView(APIView):
    """O'quvchi profili: XP, daraja, ketma-ketlik, nishonlar, statistika."""

    def get(self, request):
        u = request.user
        return Response({
            'username': u.username, 'first_name': u.first_name, 'date_joined': u.date_joined,
            **gamification.profile(u),
        })


class SubjectListView(APIView):
    """Faol fanlar ro'yxati (har birida nechta kurs borligi bilan)."""

    def get(self, request):
        qs = Subject.objects.filter(is_active=True).annotate(book_count=Count('books'))
        return Response(SubjectSerializer(qs, many=True).data)


class TopicListView(generics.ListAPIView):
    serializer_class = TopicSerializer

    def get_queryset(self):
        return Topic.objects.filter(book_id=self.kwargs['book_id'])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['topic_states'] = topic_states(self.request.user, self.get_queryset())
        return context


class BookProgressView(APIView):
    """Kitob bo'yicha talaba holati: barcha mavzu tugadimi, yakuniy imtihon/sertifikat bormi."""

    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        cert = Certificate.objects.filter(student=request.user, book=book).first()
        return Response({
            'all_topics_completed': all_topics_completed(request.user, book),
            'exam_exists': BookExam.objects.filter(book=book, status=STATUS_DONE).exists(),
            'certificate': bool(cert),
            'weak_count': len(review_service.weak_questions(request.user, book)),
        })


def _grade(questions, answers):
    """answers: {"0": chosen_index, ...}. Javob berilmagan savol xato hisoblanadi."""
    details = []
    score = 0
    for i, q in enumerate(questions):
        chosen = answers.get(str(i))
        correct = chosen == q['correct_index']
        score += int(correct)
        # To'g'ri javob ataylab qaytarilmaydi (yodlab olishning oldini olish) - faqat qayerdan o'qish kerakligi (bet).
        details.append({'index': i, 'correct': correct, 'page': q.get('page')})
    return score, len(questions), details


def _read_answers(request):
    answers = request.data.get('answers')
    if not isinstance(answers, dict):
        raise ValidationError({'answers': "answers obyekt bo'lishi kerak: {savol_indeksi: tanlangan_variant}"})
    return {str(k): v for k, v in answers.items()}


class TopicTestSubmitView(APIView):
    """Talaba mavzu testini topshiradi. 100% bo'lsa mavzu "o'tildi" deb belgilanadi."""

    def post(self, request, topic_id):
        topic = get_object_or_404(Topic, id=topic_id)
        state = topic_states(request.user, topic.book.topics.all())[topic.id]
        if not state['unlocked']:
            raise PermissionDenied("Bu mavzu hali ochilmagan: avval oldingi mavzu testini topshiring.")

        asset = GeneratedAsset.objects.filter(
            topic=topic, kind=GeneratedAsset.KIND_TOPIC_TEST, status=STATUS_DONE
        ).first()
        if not asset:
            raise ValidationError({'detail': "Bu mavzu uchun test hali yaratilmagan."})

        score, total, details = _grade(asset.data['questions'], _read_answers(request))
        passed = total > 0 and score == total
        xp = 0
        attempt = TestAttempt.objects.create(
            student=request.user, topic=topic, answers=_read_answers(request),
            score=score, total=total, passed=passed,
        )
        if passed:
            TopicCompletion.objects.get_or_create(
                student=request.user, topic=topic, defaults={'attempt': attempt}
            )
            xp = gamification.award_topic(request.user, topic)
        return Response({
            'score': score, 'total': total, 'passed': passed, 'details': details,
            'xp_gained': xp, 'streak': gamification.streak_info(request.user),
        })


class BookExamByBookView(generics.RetrieveAPIView):
    serializer_class = BookExamSerializer

    def get_object(self):
        return get_object_or_404(BookExam, book_id=self.kwargs['book_id'])


class BookExamCreateView(APIView):
    """Yakuniy imtihonni yaratish/qayta yaratish. Faqat o'qituvchi (qoida asosida, AI'siz)."""

    permission_classes = [IsTeacher]

    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        _guard_not_imported(book)
        exam, _ = BookExam.objects.get_or_create(book=book, defaults={'created_by': request.user})

        pages_by_topic = {
            topic: [
                (p.page_number, p.text)
                for p in book.pages.filter(page_number__gte=topic.start_page, page_number__lte=topic.end_page)
            ]
            for topic in book.topics.all()
        }
        try:
            exam.data = build_book_exam(book, pages_by_topic)
            exam.status = STATUS_DONE
            exam.error_message = ''
        except NotEnoughDataError as exc:
            exam.status = STATUS_FAILED
            exam.error_message = str(exc)
        exam.save()
        return Response(
            BookExamSerializer(exam, context={'request': request}).data, status=status.HTTP_200_OK
        )


class BookExamSubmitView(APIView):
    """Talaba yakuniy imtihonni topshiradi; 100% va barcha mavzu tugagan bo'lsa sertifikat beriladi."""

    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        if not all_topics_completed(request.user, book):
            raise PermissionDenied("Yakuniy imtihon uchun avval barcha mavzu testlarini topshiring.")

        exam = BookExam.objects.filter(book=book, status=STATUS_DONE).first()
        if not exam:
            raise ValidationError({'detail': "Yakuniy imtihon hali yaratilmagan."})

        answers = _read_answers(request)
        score, total, details = _grade(exam.data['questions'], answers)
        passed = total > 0 and score == total
        xp = 0
        TestAttempt.objects.create(
            student=request.user, book=book, answers=answers, score=score, total=total, passed=passed,
        )

        certificate = False
        if passed:
            if not Certificate.objects.filter(student=request.user, book=book).exists():
                name = request.user.get_full_name() or request.user.username
                pdf = build_certificate_pdf(name, book.title, timezone.now())
                cert = Certificate(student=request.user, book=book)
                cert.file.save(f'certificate_{book.id}_{request.user.id}.pdf', ContentFile(pdf), save=False)
                cert.save()
            certificate = True
            xp = gamification.award_exam(request.user, book)

        return Response({
            'score': score, 'total': total, 'passed': passed,
            'details': details, 'certificate': certificate,
            'xp_gained': xp, 'streak': gamification.streak_info(request.user),
        })


class CertificateDownloadView(APIView):
    def get(self, request, book_id):
        cert = get_object_or_404(Certificate, student=request.user, book_id=book_id)
        return FileResponse(cert.file.open('rb'), as_attachment=True, filename='sertifikat.pdf')


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

        _guard_not_imported(topic.book)
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

        _guard_not_imported(topic.book)
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


class BookImportView(APIView):
    """Tayyor JSON'dan kitobni import qilish (faqat o'qituvchi). Fayl (`file`) yoki JSON tanasi."""

    permission_classes = [IsTeacher]

    def post(self, request):
        import json

        upload = request.FILES.get('file')
        try:
            data = json.load(upload) if upload else request.data
        except (ValueError, UnicodeDecodeError):
            raise ValidationError({'detail': "Fayl to'g'ri JSON emas."})
        try:
            summary = import_book_json(data, request.user)
        except ValueError as exc:
            return Response({'errors': exc.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        return Response(summary, status=status.HTTP_201_CREATED)


class SectionListView(APIView):
    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        return Response(section_states(request.user, book))


class SectionExamByIdView(generics.RetrieveAPIView):
    serializer_class = SectionExamSerializer

    def get_object(self):
        return get_object_or_404(SectionExam, section_id=self.kwargs['section_id'])


class SectionExamSubmitView(APIView):
    """Bo'lim testi: 100% bo'lsa bo'lim "o'tildi" va keyingi bo'lim ochiladi."""

    def post(self, request, section_id):
        section = get_object_or_404(Section, id=section_id)
        topic_ids = list(section.topics.values_list('id', flat=True))
        done = TopicCompletion.objects.filter(student=request.user, topic_id__in=topic_ids).count()
        if done != len(topic_ids):
            raise PermissionDenied("Bo'lim testi uchun avval bo'limdagi barcha mavzu testlarini topshiring.")

        exam = get_object_or_404(SectionExam, section=section)
        answers = _read_answers(request)
        score, total, details = _grade(exam.data['questions'], answers)
        passed = total > 0 and score == total
        xp = 0
        TestAttempt.objects.create(
            student=request.user, section=section, answers=answers, score=score, total=total, passed=passed,
        )
        if passed:
            SectionCompletion.objects.get_or_create(student=request.user, section=section)
            xp = gamification.award_section(request.user, section)
        return Response({
            'score': score, 'total': total, 'passed': passed, 'details': details,
            'xp_gained': xp, 'streak': gamification.streak_info(request.user),
        })


class ReviewListView(APIView):
    """Xatolarni takrorlash: talaba oxirgi marta xato qilgan savollar (to'g'ri javobsiz)."""

    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        return Response({'items': review_service.public_weak(review_service.weak_questions(request.user, book))})


class ReviewAnswerView(APIView):
    """Takrorlashda javob berish: faqat to'g'ri/xato va bet qaytadi. To'g'ri javob XP beradi."""

    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        key = request.data.get('key')
        choice = request.data.get('choice')
        weak = {w['key']: w for w in review_service.weak_questions(request.user, book)}
        item = weak.get(key)
        if not item:
            raise ValidationError({'detail': "Bu savol takrorlash ro'yxatida yo'q."})
        correct = choice == item['correct_index']
        ra = ReviewAnswer.objects.create(user=request.user, book=book, qkey=key, correct=correct)
        xp = gamification.award_review(request.user, ra.id) if correct else 0
        return Response({
            'correct': correct, 'page': item['page'], 'xp_gained': xp,
            'remaining': len(weak) - (1 if correct else 0),
        })


class BookSearchView(APIView):
    """Kurs ichida qidiruv (o'quvchi uchun faqat ochilgan mavzular)."""

    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        allowed = None
        if not request.user.is_staff:
            states = topic_states(request.user, book.topics.all())
            allowed = {tid for tid, st in states.items() if st['unlocked']}
        hits = review_service.search_book(book, request.query_params.get('q', ''), allowed)
        return Response({'results': hits})
