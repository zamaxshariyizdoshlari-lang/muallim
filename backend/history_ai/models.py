from django.conf import settings
from django.db import models


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
    """Tanlangan mavzu uchun yaratilgan dars rejasi + test (AI natijasi)."""

    STATUS_PENDING = 'pending'
    STATUS_DONE = 'done'
    STATUS_FAILED = 'failed'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Kutilmoqda'),
        (STATUS_DONE, 'Tayyor'),
        (STATUS_FAILED, 'Xatolik'),
    ]

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='lessons')
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
