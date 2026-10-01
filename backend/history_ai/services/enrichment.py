"""Test savollariga import vaqtida `tag` (qaysi qism) va `level` (qiyinlik darajasi) qo'shish.

- `tag`: savol betini qamrab olgan dars blokining sarlavhasi. Xatolar tahlilida "Temirdan foydalanish"
  kabi qism nomi ko'rsatiladi. Bet bo'yicha blok topilmasa, tag qo'yilmaydi.
- `level`: savol matnidagi belgilarga ko'ra taxminiy daraja (eslash / tushunish / qo'llash).
  Bu faqat boshlang'ich taxmin; JSON'da qo'lda yozilgan qiymat har doim ustun turadi.
"""
import random
import re

UNDERSTAND = re.compile(r"nima uchun|nega|sabab|ta'sir|farq|ahamiyat|natija|oqibat|nimaga imkon|nimani oshir", re.I)
APPLY = re.compile(r"kirmaydi|quyidagilardan|qaysi biri|noto'g'ri|to'g'ri emas|mos keladi|taqqosla", re.I)


def guess_level(question):
    q = re.sub(r"[ʻ’‘ʼ`´]", "'", question)
    if APPLY.search(q):
        return 'qollash'
    if UNDERSTAND.search(q):
        return 'tushunish'
    return 'eslash'


def block_tag(blocks, page):
    if not page:
        return None
    return next((b['heading'] for b in blocks if page in (b.get('pages') or []) and b.get('heading')), None)


_ALL_OF_ABOVE = re.compile(r"hammasi|barchasi|yuqoridagi|hech biri", re.I)


def shuffle_choices(q, seed):
    """To'g'ri javob doim birinchi variant bo'lib qolmasligi uchun variantlarni aralashtiradi.

    Natija savol matni va `seed` bo'yicha aniq (deterministik): qayta import qilinganda tartib o'zgarmaydi.
    "Hammasi to'g'ri" kabi tartibga bog'liq variantli savollar va to'g'ri javobi birinchi bo'lmagan
    (qo'lda joylashtirilgan) savollar o'zgartirilmaydi.
    """
    opts = q.get('options')
    if not isinstance(opts, list) or q.get('correct_index') != 0 or len(opts) < 3:
        return q
    if any(_ALL_OF_ABOVE.search(str(o)) for o in opts):
        return q
    order = list(range(len(opts)))
    random.Random(f"{seed}:{q.get('question', '')}").shuffle(order)
    return {**q, 'options': [opts[i] for i in order], 'correct_index': order.index(0)}


def shuffle_questions(questions, seed):
    return [shuffle_choices(q, seed) if q.get('page') else q for q in questions]


def enrich_questions(questions, blocks):
    """Savollarning nusxasini qaytaradi: yetishmayotgan `level` va `tag` to'ldirilgan holda."""
    out = []
    for q in questions:
        q = dict(q)
        if q.get('page'):  # sahifaga asoslanmagan (til) kurslarida taxmin ishonchsiz - daraja qo'yilmaydi
            q.setdefault('level', guess_level(q['question']))
        if 'tag' not in q:
            tag = block_tag(blocks, q.get('page'))
            if tag:
                q['tag'] = tag
        out.append(q)
    return out
