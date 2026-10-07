"""Daraja aniqlash testi: foydalanuvchi qaysi kursdan boshlashi kerakligini aniqlaydi.

Test kurslarning o'z savollaridan tuziladi (yangi kontent kerak emas): har bir fan uchun daraja
bosqichlari (kurslar) ketma-ketligi beriladi, har bosqichdan bir nechta savol olinadi. Foydalanuvchi
birinchi o'zlashtira olmagan bosqich kursidan boshlashi tavsiya etiladi.
"""
import random

from django.db import transaction

from ..models import Book, GeneratedAsset, PlacementResult, Subject, Topic

PASS_RATIO = 0.6       # bosqich "o'zlashtirilgan" hisoblanishi uchun to'g'ri javoblar ulushi
PER_STAGE = 8          # har bosqichdan savollar soni

# fan slug -> bosqichlar (osondan qiyinga). Kurs `book` (Book.key) yoki `title_has` (sarlavhada so'z) bo'yicha
# topiladi; kurs bazada bo'lmasa bosqich o'tkazib yuboriladi.
PLACEMENTS = {
    'turk-tili': [
        {'key': 'A1', 'label': 'A1 (boshlang\'ich)', 'book': 'turk_a1'},
        {'key': 'A2', 'label': 'A2 (elementar)', 'title_has': 'A2'},
        {'key': 'B1', 'label': 'B1 (o\'rta)', 'book': 'turk_b1'},
    ],
    'tarix': [
        {'key': '6', 'label': '6-sinf darajasi', 'book': 'qadimgi-dunyo-6'},
        {'key': '7', 'label': '7-sinf darajasi', 'book': 'ozbekiston-tarixi-7'},
    ],
}


def _stages(slug):
    """Bazada kursi bor bosqichlar: [(stage, Book)]."""
    out = []
    for st in PLACEMENTS.get(slug, []):
        books = Book.objects.filter(subject__slug=slug)
        book = (
            books.filter(key=st['book']).first() if 'book' in st
            else books.filter(title__icontains=st['title_has']).first()
        )
        if book:
            out.append((st, book))
    return out


def _pool(book):
    """Kursning barcha test savollari: [(id, savol dict)]; id = '<mavzu>:<indeks>'."""
    pool = []
    topics = {t.id: t for t in Topic.objects.filter(book=book)}
    for asset in GeneratedAsset.objects.filter(topic__in=topics.values(), kind=GeneratedAsset.KIND_TOPIC_TEST):
        for i, q in enumerate((asset.data or {}).get('questions') or []):
            if 'correct_index' in q and q.get('options'):
                pool.append((f'{asset.topic_id}:{i}', q))
    return pool


def _find(qid):
    topic_id, idx = qid.split(':')
    asset = GeneratedAsset.objects.filter(topic_id=int(topic_id), kind=GeneratedAsset.KIND_TOPIC_TEST).first()
    if not asset:
        return None
    qs = (asset.data or {}).get('questions') or []
    return qs[int(idx)] if int(idx) < len(qs) else None


def available(user):
    """Daraja testi bor fanlar ro'yxati + foydalanuvchining oxirgi natijasi."""
    out = []
    for subject in Subject.objects.filter(is_active=True):
        stages = _stages(subject.slug)
        if not stages:
            continue
        last = PlacementResult.objects.filter(user=user, subject=subject).order_by('-created_at').first()
        out.append({
            'subject_slug': subject.slug, 'subject_title': subject.title,
            'stages': [s['label'] for s, _ in stages], 'questions': PER_STAGE * len(stages),
            'result': serialize_result(last) if last else None,
        })
    return out


def build_test(slug, rng=None):
    """Savollar (to'g'ri javobsiz). Har bosqichdan PER_STAGE ta tasodifiy savol, bosqich tartibida."""
    rng = rng or random.Random()
    questions = []
    for st, book in _stages(slug):
        pool = _pool(book)
        for qid, q in rng.sample(pool, min(PER_STAGE, len(pool))):
            questions.append({
                'id': qid, 'stage': st['key'], 'question': q['question'], 'options': q['options'],
            })
    return questions


def evaluate(slug, answers):
    """answers: {qid: tanlangan indeks}. -> (bosqichlar natijasi, tavsiya etilgan bosqich, o'zlashtirilgan oxirgi bosqich)."""
    stages = _stages(slug)
    per = {st['key']: {'right': 0, 'total': 0} for st, _ in stages}
    stage_of = {}
    for st, book in stages:
        stage_of.update({qid: st['key'] for qid, _ in _pool(book)})
    for qid, choice in answers.items():
        key = stage_of.get(qid)
        q = _find(qid) if key else None
        if not q:
            continue
        per[key]['total'] += 1
        per[key]['right'] += int(choice == q['correct_index'])
    mastered, start = None, None
    for st, book in stages:
        p = per[st['key']]
        ok = p['total'] > 0 and p['right'] / p['total'] >= PASS_RATIO
        if ok and start is None:
            mastered = (st, book)
        elif start is None:
            start = (st, book)
    # barcha bosqichlar o'zlashtirilgan bo'lsa, oxirgi kursni takrorlash/chuqurlashtirish tavsiya etiladi
    return per, (start or mastered), mastered


@transaction.atomic
def submit(user, slug, answers):
    subject = Subject.objects.get(slug=slug)
    per, start, mastered = evaluate(slug, answers)
    total = sum(p['total'] for p in per.values())
    right = sum(p['right'] for p in per.values())
    start_stage, start_book = start if start else (None, None)
    result = PlacementResult.objects.create(
        user=user, subject=subject, score=right, total=total, per_stage=per,
        level_key=mastered[0]['key'] if mastered else '',
        level_label=mastered[0]['label'] if mastered else "Boshlang'ich",
        recommended_book=start_book,
    )
    return result


def serialize_result(r):
    book = r.recommended_book
    return {
        'id': r.id, 'subject_slug': r.subject.slug, 'score': r.score, 'total': r.total,
        'percent': round(r.score / r.total * 100) if r.total else 0,
        'level_key': r.level_key, 'level_label': r.level_label, 'per_stage': r.per_stage,
        'recommended': {'book_id': book.id, 'title': book.title} if book else None,
        'created_at': r.created_at.isoformat(),
    }
