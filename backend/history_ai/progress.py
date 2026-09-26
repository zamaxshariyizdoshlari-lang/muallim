from .models import Certificate, TopicCompletion


def topic_states(user, topics):
    """topics (order bo'yicha) -> {topic_id: {"unlocked": bool, "completed": bool}}.

    O'qituvchi (is_staff) uchun hammasi ochiq. O'quvchi uchun mavzu faqat
    birinchi bo'lsa yoki oldingi mavzu testi 100% topshirilgan bo'lsa ochiladi.
    """
    topics = list(topics)
    completed_ids = set(
        TopicCompletion.objects.filter(student=user, topic__in=topics).values_list('topic_id', flat=True)
    )
    states = {}
    previous_completed = True
    for topic in topics:
        completed = topic.id in completed_ids
        states[topic.id] = {
            'unlocked': bool(user.is_staff) or previous_completed,
            'completed': completed,
        }
        previous_completed = completed
    return states


def all_topics_completed(user, book):
    topic_ids = list(book.topics.values_list('id', flat=True))
    if not topic_ids:
        return False
    done = TopicCompletion.objects.filter(student=user, topic_id__in=topic_ids).count()
    return done == len(topic_ids)


def has_certificate(user, book):
    return Certificate.objects.filter(student=user, book=book).exists()
