"""O'qituvchi paneli: kurs bo'yicha o'quvchilar natijasi va eng qiyin savollar."""
from collections import defaultdict

from django.contrib.auth import get_user_model
from django.db.models import Count, Max, Q

from ..models import Certificate, SectionCompletion, TestAttempt, Topic, TopicCompletion, XPEvent
from .review import _questions_for_attempt, qkey


def book_analytics(book):
    User = get_user_model()
    topics = list(Topic.objects.filter(book=book))
    total_topics = len(topics)

    attempts = (
        TestAttempt.objects.filter(Q(topic__book=book) | Q(section__book=book) | Q(book=book))
        .select_related('student').distinct()
    )
    student_ids = set(attempts.values_list('student_id', flat=True))
    users = User.objects.filter(id__in=student_ids, is_staff=False)

    done = dict(
        TopicCompletion.objects.filter(topic__book=book).values('student_id').annotate(n=Count('id'))
        .values_list('student_id', 'n')
    )
    sec_done = dict(
        SectionCompletion.objects.filter(section__book=book).values('student_id').annotate(n=Count('id'))
        .values_list('student_id', 'n')
    )
    certs = set(Certificate.objects.filter(book=book).values_list('student_id', flat=True))
    stats = {
        r['student_id']: r
        for r in attempts.values('student_id').annotate(n=Count('id'), last=Max('created_at'))
    }
    xp = dict(
        XPEvent.objects.filter(user_id__in=student_ids).values('user_id')
        .annotate(n=Count('id')).values_list('user_id', 'n')
    )

    students = []
    for u in users:
        st = stats.get(u.id, {})
        students.append({
            'id': u.id, 'username': u.username, 'name': u.first_name,
            'topics_done': done.get(u.id, 0), 'sections_done': sec_done.get(u.id, 0),
            'attempts': st.get('n', 0), 'last_active': st.get('last'),
            'certificate': u.id in certs,
        })
    students.sort(key=lambda s: (-s['topics_done'], s['username']))

    # Eng qiyin savollar: eng ko'p xato qilinganlar
    cache, agg, meta = {}, defaultdict(lambda: [0, 0]), {}
    for att in attempts.filter(student__is_staff=False):
        qs = _questions_for_attempt(att, cache)
        for i, q in enumerate(qs):
            key = qkey(q['question'])
            agg[key][1] += 1
            if (att.answers or {}).get(str(i)) != q['correct_index']:
                agg[key][0] += 1
            meta[key] = q
    hard = []
    for key, (wrong, seen) in agg.items():
        if seen >= 3 and wrong:
            q = meta[key]
            page = q.get('page')
            topic = next((t for t in topics if page and t.start_page <= page <= t.end_page), None)
            hard.append({
                'question': q['question'], 'page': page, 'topic_title': topic.title if topic else '',
                'wrong': wrong, 'seen': seen, 'error_rate': round(wrong / seen * 100),
            })
    hard.sort(key=lambda h: (-h['error_rate'], -h['seen']))

    return {
        'summary': {
            'students': len(students),
            'total_topics': total_topics,
            'certificates': len(certs & student_ids),
            'avg_progress': round(
                sum(s['topics_done'] for s in students) / (len(students) * total_topics) * 100
            ) if students and total_topics else 0,
        },
        'students': students,
        'hard_questions': hard[:10],
    }
