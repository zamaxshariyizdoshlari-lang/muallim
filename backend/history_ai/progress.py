from .models import Certificate, SectionCompletion, TopicCompletion


def topic_states(user, topics):
    """topics (order bo'yicha) -> {topic_id: {"unlocked": bool, "completed": bool}}.

    O'qituvchi (is_staff) uchun hammasi ochiq. O'quvchi uchun mavzu ochiladi, agar
    oldingi mavzu testi 100% topshirilgan bo'lsa VA (mavzu keyingi bo'limda bo'lsa)
    oldingi bo'lim testi ham 100% topshirilgan bo'lsa.
    """
    topics = list(topics)
    completed_ids = set(
        TopicCompletion.objects.filter(student=user, topic__in=topics).values_list('topic_id', flat=True)
    )
    section_order = []
    for t in topics:
        if t.section_id and t.section_id not in section_order:
            section_order.append(t.section_id)
    completed_sections = set(
        SectionCompletion.objects.filter(student=user, section_id__in=section_order)
        .values_list('section_id', flat=True)
    )

    states = {}
    previous_completed = True
    for topic in topics:
        completed = topic.id in completed_ids
        section_ok = True
        if topic.section_id:
            idx = section_order.index(topic.section_id)
            section_ok = idx == 0 or section_order[idx - 1] in completed_sections
        states[topic.id] = {
            'unlocked': bool(user.is_staff) or (previous_completed and section_ok),
            'completed': completed,
        }
        previous_completed = completed
    return states


def section_states(user, book):
    """Bo'limlar ro'yxati: bo'lim testi ochiqmi (barcha mavzu o'tilganmi) va topshirilganmi."""
    sections = list(book.sections.prefetch_related('topics'))
    completed_topics = set(
        TopicCompletion.objects.filter(student=user, topic__book=book).values_list('topic_id', flat=True)
    )
    completed_sections = set(
        SectionCompletion.objects.filter(student=user, section__book=book).values_list('section_id', flat=True)
    )
    result = []
    for s in sections:
        topic_ids = [t.id for t in s.topics.all()]
        result.append({
            'id': s.id, 'title': s.title, 'order': s.order,
            'exam_available': bool(topic_ids) and all(i in completed_topics for i in topic_ids),
            'completed': s.id in completed_sections,
            'has_exam': hasattr(s, 'exam'),
        })
    return result


def all_topics_completed(user, book):
    """Yakuniy imtihon uchun: barcha mavzu (va bo'lim bo'lsa barcha bo'lim testi) topshirilgan."""
    topic_ids = list(book.topics.values_list('id', flat=True))
    if not topic_ids:
        return False
    done = TopicCompletion.objects.filter(student=user, topic_id__in=topic_ids).count()
    if done != len(topic_ids):
        return False
    section_ids = list(book.sections.values_list('id', flat=True))
    if section_ids:
        return SectionCompletion.objects.filter(student=user, section_id__in=section_ids).count() == len(section_ids)
    return True


def has_certificate(user, book):
    return Certificate.objects.filter(student=user, book=book).exists()
