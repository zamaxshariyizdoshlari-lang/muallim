"""Talabaning shaxsiy tahlili: mavzu bo'yicha natijalar, imtihon dinamikasi, taxminiy natija."""
from ..models import TestAttempt, Topic
from .final_exam import level_for

WEAK_PERCENT = 75


def student_analytics(user, book):
    attempts = list(TestAttempt.objects.filter(student=user).filter(
        topic__book=book).select_related('topic').order_by('created_at'))
    by_topic = {}
    for a in attempts:
        pct = round(a.score / a.total * 100) if a.total else 0
        t = by_topic.setdefault(a.topic_id, {
            'topic_id': a.topic_id, 'title': a.topic.title, 'attempts': 0, 'best': 0, 'last': 0,
        })
        t['attempts'] += 1
        t['best'] = max(t['best'], pct)
        t['last'] = pct
    topics = sorted(by_topic.values(), key=lambda t: t['last'])
    exams = [
        {'date': a.created_at.date().isoformat(), 'percent': round(a.score / a.total * 100) if a.total else 0,
         'passed': a.passed}
        for a in TestAttempt.objects.filter(student=user, book=book).order_by('created_at')
    ]
    recent = [e['percent'] for e in exams[-3:]]
    forecast = round(sum(recent) / len(recent)) if recent else None
    untouched = [
        {'topic_id': t.id, 'title': t.title}
        for t in Topic.objects.filter(book=book).exclude(id__in=by_topic)
    ]
    return {
        'topics': topics,
        'weak': [t for t in topics if t['last'] < WEAK_PERCENT][:5],
        'untouched': untouched,
        'exams': exams,
        'forecast': forecast,
        'forecast_level': level_for(forecast) if forecast is not None else None,
    }
