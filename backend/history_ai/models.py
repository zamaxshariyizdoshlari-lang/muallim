from django.conf import settings
from django.db import models

STATUS_PENDING = 'pending'
STATUS_DONE = 'done'
STATUS_FAILED = 'failed'
STATUS_CHOICES = [
    (STATUS_PENDING, 'Kutilmoqda'),
    (STATUS_DONE, 'Tayyor'),
    (STATUS_FAILED, 'Xatolik'),
]


class Book(models.Model):
    """O'qituvchi tomonidan yuklangan tarix darsligi (PDF)."""

    title = models.CharField(max_length=255)
    # JSON orqali import qilingan kitoblarda PDF faylning o'zi bo'lmaydi.
    file = models.FileField(upload_to='books/', blank=True)
    # JSON import shu kalit bo'yicha kitobni topib yangilaydi.
    key = models.CharField(max_length=100, blank=True, db_index=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='books'
    )
    # Kelajakda ERP'dagi School modeliga FK bilan almashtiriladi; hozircha ixtiyoriy id sifatida.
    school_id_ref = models.IntegerField(null=True, blank=True)
    has_text_layer = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Page(models.Model):
    """Kitobning bitta beti, bet raqami bilan matn."""

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='pages')
    page_number = models.PositiveIntegerField()
    text = models.TextField(blank=True)

    class Meta:
        ordering = ['page_number']
        unique_together = ('book', 'page_number')

    def __str__(self):
        return f"{self.book.title} - bet {self.page_number}"


class Section(models.Model):
    """Kitob bo'limi (masalan "I BO'LIM"): bir nechta mavzuni birlashtiradi."""

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='sections')
    key = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        unique_together = ('book', 'key')

    def __str__(self):
        return self.title


class Topic(models.Model):
    """Kitobdan aniqlangan bob/paragraf (mavzu)."""

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='topics')
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True, related_name='topics')
    key = models.CharField(max_length=50, blank=True)
    title = models.CharField(max_length=255)
    start_page = models.PositiveIntegerField()
    end_page = models.PositiveIntegerField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.title} ({self.start_page}-{self.end_page})"


class Lesson(models.Model):
    """Tanlangan mavzu uchun yaratilgan dars rejasi + test (AI natijasi).

    Mavzu uchun bitta lesson (OneToOne) - qayta yaratish shu yozuvni yangilaydi,
    har safar yangi qator qo'shilmaydi (AI chaqiruvini keraksiz takrorlamaslik uchun).
    """

    topic = models.OneToOneField(Topic, on_delete=models.CASCADE, related_name='lesson')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lessons'
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    ai_provider = models.CharField(max_length=20, blank=True)

    lesson_plan = models.JSONField(null=True, blank=True)
    quiz = models.JSONField(null=True, blank=True)
    error_message = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dars: {self.topic.title} [{self.status}]"


class GeneratedAsset(models.Model):
    """Taqdimot yoki o'yin kabi qo'shimcha AI natijalari (mavzu bo'yicha).

    Lesson'dan alohida, chunki har biri mustaqil ravishda yaratiladi/qayta
    yaratiladi va o'z holatiga (pending/done/failed) ega bo'ladi.
    """

    KIND_PRESENTATION = 'presentation'
    KIND_GAME_TIMELINE = 'game_timeline'
    KIND_GAME_MATCHING = 'game_matching'
    KIND_GAME_FILL_BLANK = 'game_fill_blank'
    KIND_TOPIC_TEST = 'topic_test'
    KIND_CHOICES = [
        (KIND_PRESENTATION, 'Taqdimot'),
        (KIND_GAME_TIMELINE, "O'yin: xronologiya"),
        (KIND_GAME_MATCHING, "O'yin: moslashtirish"),
        (KIND_GAME_FILL_BLANK, "O'yin: bo'sh joyni to'ldirish"),
        (KIND_TOPIC_TEST, "Mavzu bo'yicha to'liq test"),
    ]

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='assets')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='generated_assets'
    )
    kind = models.CharField(max_length=20, choices=KIND_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    ai_provider = models.CharField(max_length=20, blank=True)

    data = models.JSONField(null=True, blank=True)
    error_message = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('topic', 'kind')

    def __str__(self):
        return f"{self.get_kind_display()}: {self.topic.title} [{self.status}]"


class BookExam(models.Model):
    """Kitob yakunidagi umumiy test (barcha mavzular faktlaridan quriladi).

    GeneratedAsset'ga o'xshaydi, lekin mavzu emas, kitob darajasida - shuning
    uchun alohida model (bitta kitobda bitta yakuniy imtihon).
    """

    book = models.OneToOneField(Book, on_delete=models.CASCADE, related_name='exam')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='book_exams'
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    data = models.JSONField(null=True, blank=True)
    error_message = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Yakuniy imtihon: {self.book.title} [{self.status}]"


class TestAttempt(models.Model):
    """Talabaning mavzu testi yoki kitob yakuniy imtihoniga bitta urinishi.

    Aynan bittasi to'ldiriladi: topic (mavzu testi) yoki book (yakuniy imtihon).
    """

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='test_attempts'
    )
    topic = models.ForeignKey(
        Topic, on_delete=models.CASCADE, related_name='attempts', null=True, blank=True
    )
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name='exam_attempts', null=True, blank=True
    )
    section = models.ForeignKey(
        Section, on_delete=models.CASCADE, related_name='attempts', null=True, blank=True
    )
    answers = models.JSONField()  # {"0": chosen_index, "1": chosen_index, ...}
    score = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    passed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        target = self.topic.title if self.topic_id else f"Yakuniy: {self.book.title}"
        return f"{self.student.username} - {target} - {self.score}/{self.total}"


class TopicCompletion(models.Model):
    """Talaba shu mavzu testini 100% to'g'ri topshirganini bildiradi (mavzu ochilishi uchun asos)."""

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='topic_completions'
    )
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='completions')
    attempt = models.ForeignKey(TestAttempt, on_delete=models.SET_NULL, null=True, blank=True)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'topic')

    def __str__(self):
        return f"{self.student.username} - {self.topic.title} - o'tildi"


class Certificate(models.Model):
    """Talaba butun kitobni (barcha mavzu + yakuniy imtihon) tugatganda beriladi."""

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='certificates'
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='certificates')
    file = models.FileField(upload_to='certificates/')
    issued_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'book')

    def __str__(self):
        return f"Sertifikat: {self.student.username} - {self.book.title}"


class SectionExam(models.Model):
    """Bo'lim testi (JSON importda bo'limdagi mavzu testlaridan tuziladi)."""

    section = models.OneToOneField(Section, on_delete=models.CASCADE, related_name='exam')
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Bo'lim testi: {self.section.title}"


class SectionCompletion(models.Model):
    """Talaba bo'lim testini 100% topshirgan (keyingi bo'lim ochilishi uchun asos)."""

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='section_completions'
    )
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='completions')
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'section')
