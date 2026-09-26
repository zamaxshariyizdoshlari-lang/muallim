"""Xatolarni takrorlash va kurs ichida qidiruv.

"Zaif savol" - talaba oxirgi marta xato javob bergan (rasmiy testda yoki takrorlashda) savol.
Savol matni bo'yicha kalit (qkey) hisoblanadi, shuning uchun test qayta yaratilsa ham izchil.
"""
import hashlib
import re

from ..models import (
    STATUS_DONE, BookExam, GeneratedAsset, Lesson, ReviewAnswer, SectionExam, TestAttempt, Topic,
)


def qkey(text):
    return hashlib.sha1(text.strip().encode('utf-8')).hexdigest()[:12]


def _questions_for_attempt(attempt, cache):
    if attempt.topic_id:
        key = ('t', attempt.topic_id)
        if key not in cache:
            a = GeneratedAsset.objects.filter(
                topic_id=attempt.topic_id, kind=GeneratedAsset.KIND_TOPIC_TEST, status=STATUS_DONE
            ).first()
            cache[key] = (a.data or {}).get('questions', []) if a else []
    elif attempt.section_id:
        key = ('s', attempt.section_id)
        if key not in cache:
            e = SectionExam.objects.filter(section_id=attempt.section_id).first()
            cache[key] = (e.data or {}).get('questions', []) if e else []
    else:
        key = ('b', attempt.book_id)
        if key not in cache:
            e = BookExam.objects.filter(book_id=attempt.book_id, status=STATUS_DONE).first()
            cache[key] = (e.data or {}).get('questions', []) if e else []
    return cache[key]


def weak_questions(user, book):
    """Talaba hozir noto'g'ri deb turgan savollar ro'yxati (to'liq savol, correct_index bilan - ichki)."""
    events = []  # (vaqt, qkey, to'g'rimi, savol)
    cache = {}
    attempts = TestAttempt.objects.filter(student=user).filter(
        topic__book=book
    ) | TestAttempt.objects.filter(student=user, section__book=book) | TestAttempt.objects.filter(
        student=user, book=book
    )
    for att in attempts.distinct():
        qs = _questions_for_attempt(att, cache)
        for i, q in enumerate(qs):
            chosen = (att.answers or {}).get(str(i))
            events.append((att.created_at, qkey(q['question']), chosen == q['correct_index'], q))
    for ra in ReviewAnswer.objects.filter(user=user, book=book):
        events.append((ra.created_at, ra.qkey, ra.correct, None))

    events.sort(key=lambda e: e[0])
    state, questions = {}, {}
    for _, key, ok, q in events:
        state[key] = ok
        if q is not None:
            questions[key] = q

    topics = list(Topic.objects.filter(book=book))
    weak = []
    for key, ok in state.items():
        if ok or key not in questions:
            continue
        q = questions[key]
        page = q.get('page')
        topic = next((t for t in topics if page and t.start_page <= page <= t.end_page), None)
        weak.append({
            'key': key, 'question': q['question'], 'options': q['options'], 'page': page,
            'correct_index': q['correct_index'],
            'topic_id': topic.id if topic else None, 'topic_title': topic.title if topic else '',
        })
    weak.sort(key=lambda w: (w['page'] or 0))
    return weak


def public_weak(items):
    return [{k: v for k, v in w.items() if k != 'correct_index'} for w in items]


def _snippet(text, needle, radius=70):
    m = re.search(re.escape(needle), text, flags=re.IGNORECASE)
    if not m:
        return text[: radius * 2]
    a, b = max(0, m.start() - radius), min(len(text), m.end() + radius)
    return ('...' if a else '') + text[a:b].replace('\n', ' ') + ('...' if b < len(text) else '')


def search_book(book, query, topic_ids=None, limit=20):
    """Mavzu sarlavhasi, tushuntirish matni va muhim faktlar bo'yicha oddiy qidiruv."""
    q = query.strip()
    if len(q) < 2:
        return []
    hits = []
    lessons = Lesson.objects.filter(topic__book=book, lesson_plan__isnull=False).select_related('topic')
    for lesson in lessons:
        t = lesson.topic
        if topic_ids is not None and t.id not in topic_ids:
            continue
        plan = lesson.lesson_plan or {}
        found = None
        if q.lower() in t.title.lower():
            found = {'snippet': t.title, 'page': t.start_page}
        if not found:
            for b in plan.get('blocks', []):
                if q.lower() in (b.get('text') or '').lower() or q.lower() in (b.get('heading') or '').lower():
                    pages = b.get('pages') or [t.start_page]
                    found = {'snippet': _snippet(b.get('text') or b.get('heading'), q), 'page': pages[0]}
                    break
        if not found:
            for f in plan.get('key_facts', []):
                if q.lower() in (f.get('fact') or '').lower():
                    found = {'snippet': f['fact'], 'page': f.get('page')}
                    break
        if found:
            hits.append({'topic_id': t.id, 'topic_title': t.title, **found})
    hits.sort(key=lambda h: h['page'] or 0)
    return hits[:limit]
