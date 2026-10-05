"""Talaba bosh sahifasi: kurslar bo'yicha progress, "davom etish" mavzusi, bugungi takrorlash soni."""
from django.utils import timezone

from ..models import Book, ReviewCard, TestAttempt, Topic, TopicCompletion
from ..progress import topic_states


def student_dashboard(user):
    today = timezone.localdate()
    started_books = set(
        TestAttempt.objects.filter(student=user).exclude(topic=None).values_list('topic__book_id', flat=True)
    ) | set(TopicCompletion.objects.filter(student=user).values_list('topic__book_id', flat=True))
    due = {}
    for bid in ReviewCard.objects.filter(user=user, due_date__lte=today).values_list('book_id', flat=True):
        due[bid] = due.get(bid, 0) + 1

    courses = []
    for book in Book.objects.select_related('subject').order_by('id'):
        topics = list(Topic.objects.filter(book=book).order_by('order', 'id'))
        if not topics:
            continue
        states = topic_states(user, topics)
        done = sum(1 for t in topics if states[t.id]['completed'])
        nxt = next((t for t in topics if states[t.id]['unlocked'] and not states[t.id]['completed']), None)
        courses.append({
            'id': book.id, 'title': book.title,
            'subject': book.subject.title if book.subject_id else '',
            'subject_slug': book.subject.slug if book.subject_id else '',
            'topics_total': len(topics), 'topics_done': done,
            'percent': round(done / len(topics) * 100),
            'started': book.id in started_books or done > 0,
            'next_topic': {'id': nxt.id, 'title': nxt.title} if nxt else None,
            'due_reviews': due.get(book.id, 0),
        })

    mine = sorted((c for c in courses if c['started']), key=lambda c: (c['percent'] == 100, -c['percent']))
    cont = next((c for c in mine if c['next_topic']), None)
    return {
        'courses': courses,
        'continue': {
            'book_id': cont['id'], 'book_title': cont['title'], 'topic': cont['next_topic'],
            'percent': cont['percent'],
        } if cont else None,
        'due_reviews_total': sum(due.values()),
        'due_book_id': max(due, key=due.get) if due else None,
    }
