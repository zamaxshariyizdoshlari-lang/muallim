import uuid

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


class Subject(models.Model):
    """Fan (Tarix, Turk tili, ...). Har fanda bir nechta kurs (kitob) bo'ladi."""

    slug = models.SlugField(max_length=50, unique=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300, blank=True)
    # lucide-react ikonka nomi (frontend xaritalaydi), masalan "landmark", "languages"
    icon = models.CharField(max_length=40, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.title


class Book(models.Model):
    """Kurs (darslik): bo'limlar -> mavzular. PDF yoki tayyor JSON orqali yaratiladi."""

    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name='books')
    description = models.CharField(max_length=500, blank=True)

    title = models.CharField(max_length=255)
    # JSON orqali import qilingan kitoblarda PDF faylning o'zi bo'lmaydi.
    file = models.FileField(upload_to='books/', blank=True)
    # JSON import shu kalit bo'yicha kitobni topib yangilaydi.
    key = models.CharField(max_length=100, blank=True, db_index=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='books'
    )
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


def _new_certificate_code():
    return uuid.uuid4().hex[:10].upper()


class Certificate(models.Model):
    """Talaba butun kitobni (barcha mavzu + yakuniy imtihon) tugatganda beriladi.

    `code` - istalgan kishi (masalan ish beruvchi) sertifikatni ochiq havola orqali tekshirishi
    uchun (talaba yoki kitob ID'siz, taxmin qilib bo'lmaydigan tasodifiy kod).
    """

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='certificates'
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='certificates')
    file = models.FileField(upload_to='certificates/')
    code = models.CharField(max_length=12, unique=True, default=_new_certificate_code, editable=False)
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


class XPEvent(models.Model):
    """Bir martalik ball mukofoti jurnali (user + kind + ref unikal: qayta topshirish ball bermaydi)."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='xp_events')
    kind = models.CharField(max_length=20)
    ref_id = models.PositiveIntegerField()
    points = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'kind', 'ref_id')
        verbose_name = 'Ball voqeasi'
        verbose_name_plural = 'Ball voqealari'

    def __str__(self):
        return f"{self.user} +{self.points} ({self.kind})"


class ReviewAnswer(models.Model):
    """Xatolarni takrorlash rejimida berilgan javob (savol matni kaliti bo'yicha)."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='review_answers')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='review_answers')
    qkey = models.CharField(max_length=20, db_index=True)
    correct = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)


class UserSettings(models.Model):
    """Foydalanuvchi sozlamalari: kunlik maqsad (ball) va haftalik reytingda ko'rinish."""

    GOAL_CHOICES = (20, 50, 100)

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='learning_settings')
    daily_goal = models.PositiveIntegerField(default=50)
    show_in_leaderboard = models.BooleanField(default=True)
    email_reminders = models.BooleanField(default=True, verbose_name="Streak eslatma emaillari")
    last_reminder_sent = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Foydalanuvchi sozlamasi"
        verbose_name_plural = "Foydalanuvchi sozlamalari"

    def __str__(self):
        return f"{self.user} maqsad={self.daily_goal}"


class ReviewCard(models.Model):
    """Oraliq takrorlash (spaced repetition) kartochkasi: talaba xato qilgan savol.

    To'g'ri javob berilganda interval kattalashadi (kartochka uzoqroq muddatga "uxlaydi");
    oxirgi intervalda ham to'g'ri javob berilsa o'zlashtirilgan hisoblanib o'chiriladi.
    Xato javob interval'ni 0 ga qaytaradi (kartochka darhol yana "sana"si kelgan bo'ladi).
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='review_cards')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='review_cards')
    qkey = models.CharField(max_length=20, db_index=True)
    data = models.JSONField()  # {question, options, correct_index, page, topic_id, topic_title}
    interval_idx = models.PositiveSmallIntegerField(default=0)
    due_date = models.DateField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'book', 'qkey')

    def __str__(self):
        return f"{self.user} · {self.qkey} (due {self.due_date})"


class DailyActivity(models.Model):
    """Talabaning har kuni platformada faol bo'lgan vaqti (soniyada).

    Frontend sahifa ochiq va faol bo'lganda har 30 soniyada heartbeat yuboradi;
    admin panelda foydalanuvchi qaysi kuni qancha vaqt o'tirganini shu orqali ko'radi.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='daily_activity')
    date = models.DateField(db_index=True)
    seconds_active = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'date')
        verbose_name = "Kunlik faollik"
        verbose_name_plural = "Kunlik faollik"
        ordering = ['-date']

    def __str__(self):
        return f"{self.user} — {self.date} ({self.seconds_active}s)"
