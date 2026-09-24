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
    file = models.FileField(upload_to='books/')
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


class Topic(models.Model):
    """Kitobdan aniqlangan bob/paragraf (mavzu)."""

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='topics')
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
    KIND_CHOICES = [
        (KIND_PRESENTATION, 'Taqdimot'),
        (KIND_GAME_TIMELINE, "O'yin: xronologiya"),
        (KIND_GAME_MATCHING, "O'yin: moslashtirish"),
        (KIND_GAME_FILL_BLANK, "O'yin: bo'sh joyni to'ldirish"),
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
