"""Xatolarni takrorlash (oraliq takrorlash / spaced repetition) va kurs ichida qidiruv.

Talaba xato qilgan savol kartochka (ReviewCard) sifatida saqlanadi, "sana"si bugun bo'lganda
takrorlash ro'yxatida chiqadi. To'g'ri javob berilganda kartochka uzoqroq muddatga o'tadi
(1, 3, 7, 14, 30 kun); oxirgisida ham to'g'ri javob berilsa o'zlashtirilgan hisoblanib o'chadi.
Xato javob kartochkani darhol yana bugungi kunga qaytaradi. Savol matni bo'yicha kalit (qkey)
hisoblanadi, shuning uchun test qayta yaratilsa ham izchil qoladi.
"""
import hashlib
import re
from datetime import timedelta

from django.utils import timezone

from ..models import STATUS_DONE, BookExam, GeneratedAsset, Lesson, ReviewCard, SectionExam, Topic

INTERVALS = [1, 3, 7, 14, 30]  # kun: har to'g'ri javobdan keyingi keyingi "sana"gacha


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


def _topic_for_page(topics, page):
    if not page:
        return None
    return next((t for t in topics if t.start_page <= page <= t.end_page), None)


def _advance(user, book, key):
    """To'g'ri javob: kartochka bor bo'lsa keyingi intervalga o'tadi, oxirgisida o'zlashtirilib o'chadi."""
    card = ReviewCard.objects.filter(user=user, book=book, qkey=key).first()
    if not card:
        return
    nxt = card.interval_idx + 1
    if nxt >= len(INTERVALS):
        card.delete()
        return
    card.interval_idx = nxt
    card.due_date = timezone.localdate() + timedelta(days=INTERVALS[nxt])
    card.save(update_fields=['interval_idx', 'due_date', 'updated_at'])


def _reset(user, book, key, q, topic):
    """Xato javob: kartochka yaratiladi (yoki 0-intervalga qaytadi), bugun takrorlash uchun tayyor."""
    data = {
        'question': q['question'], 'options': q['options'], 'correct_index': q['correct_index'],
        'page': q.get('page'), 'topic_id': topic.id if topic else None, 'topic_title': topic.title if topic else '',
    }
    ReviewCard.objects.update_or_create(
        user=user, book=book, qkey=key,
        defaults={'data': data, 'interval_idx': 0, 'due_date': timezone.localdate()},
    )


def record_grading(user, book, questions, answers, topic=None):
    """Har qanday test (mavzu/bo'lim/yakuniy) topshirilgandan keyin chaqiriladi: takrorlash
    kartochkalarini yangilaydi (xato -> kartochka, to'g'ri -> mavjud kartochka ilgarilaydi).

    Hozircha faqat bitta tanlovli (mcq) savollar takrorlash tizimiga tushadi - "takrorlash"
    ekrani variant tanlash asosida ishlaydi, erkin matn/tartiblash savollarini hali qo'llamaydi.
    """
    topics = None
    for i, q in enumerate(questions):
        if q.get('type', 'mcq') != 'mcq':
            continue
        chosen = (answers or {}).get(str(i))
        correct = chosen == q['options'][q['correct_index']]
        key = qkey(q['question'])
        if correct:
            _advance(user, book, key)
        else:
            t = topic
            if t is None:
                if topics is None:
                    topics = list(Topic.objects.filter(book=book))
                t = _topic_for_page(topics, q.get('page'))
            _reset(user, book, key, q, t)


def due_cards(user, book):
    """Bugun (yoki undan oldin) "sana"si kelgan takrorlash kartochkalari."""
    return list(
        ReviewCard.objects.filter(user=user, book=book, due_date__lte=timezone.localdate())
        .order_by('due_date', 'id')
    )


def public_card(card):
    d = card.data
    return {
        'key': card.qkey, 'question': d['question'], 'options': d['options'],
        'page': d.get('page'), 'topic_id': d.get('topic_id'), 'topic_title': d.get('topic_title'),
    }


def answer_card(user, book, key, choice):
    """Takrorlashda javob berish. Qaytaradi: to'g'ri/xato, bet, o'zlashtirildimi va keyingi sana (kun)."""
    card = ReviewCard.objects.filter(user=user, book=book, qkey=key).first()
    if not card:
        return None
    correct = choice == card.data['correct_index']
    page = card.data.get('page')
    if correct:
        next_in_days = INTERVALS[card.interval_idx + 1] if card.interval_idx + 1 < len(INTERVALS) else None
        _advance(user, book, key)
        mastered = next_in_days is None
    else:
        mastered, next_in_days = False, INTERVALS[0]
        card.interval_idx = 0
        card.due_date = timezone.localdate()
        card.save(update_fields=['interval_idx', 'due_date', 'updated_at'])
    explain = None
    if not correct:
        topic = Topic.objects.filter(id=card.data.get('topic_id')).first() if card.data.get('topic_id') else None
        explain = explain_page(book, page, topic=topic)
    return {'correct': correct, 'page': page, 'mastered': mastered, 'next_in_days': next_in_days, 'explain': explain}


def explain_page(book, page, topic=None):
    """Xato javobdan keyingi qisqa eslatma: tegishli dars blokining sarlavhasi va boshi.

    `topic` berilsa (mavzu testi kabi mavzu aniq bo'lganda) shu mavzuning darsidan, aks holda
    `page` (kitob beti) orqali mos darsdan qidiriladi - sahifa raqami bo'lmagan kurslarda
    (masalan til darslari) `topic` orqali ham ishlaydi.
    """
    if topic is not None:
        lesson = Lesson.objects.filter(topic=topic, lesson_plan__isnull=False).first()
    elif page:
        lesson = Lesson.objects.filter(
            topic__book=book, topic__start_page__lte=page, topic__end_page__gte=page, lesson_plan__isnull=False,
        ).first()
    else:
        return None
    if not lesson:
        return None
    blocks = (lesson.lesson_plan or {}).get('blocks', [])
    block = None
    if page:
        block = next((b for b in blocks if page in (b.get('pages') or [])), None)
    if block is None and topic is not None:
        block = blocks[0] if blocks else None
    if block is None:
        return None
    text = block.get('text') or ''
    snippet = text[:180]
    if len(snippet) < len(text):
        snippet = snippet.rsplit(' ', 1)[0] + '...'
    return {'heading': block.get('heading', ''), 'snippet': snippet}


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


def book_dictionary(book, topic_ids=None, query=''):
    """Til kursi bo'yicha to'plangan lug'at: barcha ochilgan mavzulardagi so'zlar, bitta
    qidiriladigan ro'yxatda (har birida qaysi mavzuda o'rgatilganligi ko'rsatiladi).

    Foydalanuvchi oldin o'qigan darslarning so'zlarini alohida har bir Lesson'ni qayta
    ochmasdan, bitta joydan qidirib topishi uchun.
    """
    q = query.strip().lower()
    words = []
    lessons = Lesson.objects.filter(topic__book=book, lesson_plan__isnull=False).select_related('topic')
    for lesson in lessons:
        t = lesson.topic
        if topic_ids is not None and t.id not in topic_ids:
            continue
        for v in (lesson.lesson_plan or {}).get('vocabulary') or []:
            tr, uz = v.get('tr', ''), v.get('uz', '')
            if q and q not in tr.lower() and q not in uz.lower():
                continue
            words.append({
                'tr': tr, 'uz': uz,
                'example_tr': v.get('example_tr'), 'example_uz': v.get('example_uz'),
                'topic_id': t.id, 'topic_title': t.title,
            })
    words.sort(key=lambda w: w['tr'].lower())
    return words
