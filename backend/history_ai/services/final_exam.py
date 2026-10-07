"""Kurs yakunidagi imtihon: har urinishda butun kursdan yangi, mavzular bo'yicha teng taqsimlangan savollar.

Maqsad - sertifikat kursning haqiqiy darajasini tasdiqlashi: umumiy natija yuqori bo'lishi VA har bir
bo'limdan minimal daraja olinishi shart (bir bo'limni bilmay, boshqasini yodlab o'tib bo'lmaydi).
Savollar mavzu testlari + dars ichidagi o'qish/tinglash/gap mashqlari savollaridan olinadi; avvalgi
urinishlarda chiqqan savollar iloji boricha takrorlanmaydi.
"""
import random
from collections import defaultdict

from django.conf import settings

from ..models import ExamSession, GeneratedAsset, Lesson, Topic

EXAM_SIZE = 60
SECTION_MIN_PERCENT = 60


def final_pass_percent():
    return getattr(settings, 'FINAL_EXAM_PASS_PERCENT', 85)


def _mcq(q, topic):
    if not q.get('options') or 'correct_index' not in q:
        return None
    return {
        'question': q.get('question') or q.get('prompt'), 'options': q['options'],
        'correct_index': q['correct_index'], 'page': q.get('page'), 'tag': q.get('tag'), 'level': q.get('level'),
        'explanation': q.get('explanation'), 'topic_id': topic.id, 'section_id': topic.section_id,
    }


def topic_pool(topic):
    out = []
    asset = GeneratedAsset.objects.filter(topic=topic, kind=GeneratedAsset.KIND_TOPIC_TEST).first()
    for q in ((asset.data or {}).get('questions') or []) if asset else []:
        m = _mcq(q, topic)
        if m:
            out.append(m)
    lesson = Lesson.objects.filter(topic=topic).first()
    plan = (lesson.lesson_plan if lesson else None) or {}
    extra = []
    extra += (plan.get('reading') or {}).get('questions') or []
    extra += (plan.get('listening') or {}).get('questions') or []
    extra += [p for p in plan.get('sentence_practice') or [] if p.get('type') == 'choice']
    for q in extra:
        m = _mcq(q, topic)
        if m:
            out.append(m)
    return out


def draw(user, book, size=EXAM_SIZE, rng=None):
    rng = rng or random.Random()
    seen = set()
    for s in ExamSession.objects.filter(user=user, book=book)[:2]:
        seen |= {q['question'] for q in s.questions}
    pools = {}
    for t in Topic.objects.filter(book=book).order_by('order'):
        pool = topic_pool(t)
        rng.shuffle(pool)
        pool.sort(key=lambda q: q['question'] in seen)  # ko'rilmaganlari oldinda
        if pool:
            pools[t.id] = pool
    chosen, i = [], 0
    ids = list(pools)
    while len(chosen) < size and ids:
        tid = ids[i % len(ids)]
        if pools[tid]:
            chosen.append(pools[tid].pop(0))
        else:
            ids.remove(tid)
            continue
        i += 1
    rng.shuffle(chosen)
    session = ExamSession.objects.create(user=user, book=book, questions=chosen)
    return session


def public_questions(session):
    return [{'question': q['question'], 'options': q['options']} for q in session.questions]


def evaluate(session, answers):
    """-> (score, total, details, per_section, passed, reason)."""
    sections = defaultdict(lambda: [0, 0])
    score, details = 0, []
    for i, q in enumerate(session.questions):
        ok = answers.get(str(i)) == q['correct_index']
        score += int(ok)
        sections[q['section_id']][0] += int(ok)
        sections[q['section_id']][1] += 1
        d = {'index': i, 'correct': ok, 'page': q.get('page'), 'tag': q.get('tag'), 'level': q.get('level')}
        details.append(d)
    total = len(session.questions)
    per = [
        {'section_id': sid, 'right': r, 'total': t, 'percent': round(r / t * 100) if t else 0}
        for sid, (r, t) in sections.items()
    ]
    overall_ok = total > 0 and score * 100 >= final_pass_percent() * total
    weak = [p for p in per if p['total'] and p['percent'] < SECTION_MIN_PERCENT]
    passed = overall_ok and not weak
    reason = ''
    if not overall_ok:
        reason = f"Umumiy natija kamida {final_pass_percent()}% bo'lishi kerak."
    elif weak:
        reason = f"Har bir bo'limdan kamida {SECTION_MIN_PERCENT}% kerak: {len(weak)} ta bo'lim yetarli emas."
    return score, total, details, per, passed, reason
