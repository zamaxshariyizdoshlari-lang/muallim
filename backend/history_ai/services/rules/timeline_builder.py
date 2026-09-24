from .exceptions import NotEnoughDataError
from .extractor import extract_dated_events

MIN_ITEMS = 4
MAX_ITEMS = 8


def build_timeline(pages):
    """Sana bilan bog'liq gaplarni kod orqali ajratib, xronologik tartibda qaytaradi.

    AI ishlatilmaydi. Natija allaqachon yil bo'yicha o'sish tartibida (extract_dated_events).
    """
    events = extract_dated_events(pages)

    if len(events) < MIN_ITEMS:
        raise NotEnoughDataError(
            "Bu mavzuda aniq sanasi ko'rsatilgan voqealar yetarli emas "
            f"(topildi: {len(events)}, kamida {MIN_ITEMS} kerak)."
        )

    items = [{'label': e['text'], 'page': e['page']} for e in events[:MAX_ITEMS]]
    return {'items': items}
