from .exceptions import NotEnoughDataError
from .extractor import extract_dated_events, extract_term_definitions

MIN_PAIRS = 4
MAX_PAIRS = 8


def build_matching(pages):
    """Atama<->ta'rif juftliklarini, yetmasa sana<->voqea juftliklarini qo'shib quradi.

    AI ishlatilmaydi.
    """
    pairs = []
    used_left_labels = set()

    for t in extract_term_definitions(pages):
        if t['term'].lower() in used_left_labels:
            continue
        used_left_labels.add(t['term'].lower())
        pairs.append({'left': t['term'], 'right': t['definition'], 'page': t['page']})

    if len(pairs) < MAX_PAIRS:
        for e in extract_dated_events(pages):
            if len(pairs) >= MAX_PAIRS:
                break
            left = e['matched'] or str(e['year'])
            if left.lower() in used_left_labels:
                continue  # bir xil yil ikki marta chap tomonda bo'lsa o'yin noaniq bo'lib qoladi
            used_left_labels.add(left.lower())
            right = e['text']
            if e['matched'] and e['matched'] in right:
                right = right.replace(e['matched'], '____', 1)
            pairs.append({'left': left, 'right': right, 'page': e['page']})

    if len(pairs) < MIN_PAIRS:
        raise NotEnoughDataError(
            "Bu mavzuda moslashtirish o'yini uchun yetarli atama/sana topilmadi "
            f"(topildi: {len(pairs)}, kamida {MIN_PAIRS} kerak)."
        )

    return {'pairs': pairs[:MAX_PAIRS]}
