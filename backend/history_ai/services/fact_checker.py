"""AI natijasidagi faktlarni kitob manba matniga solishtirib tekshirish.

To'liq NLP emas — regex bilan ajratilgan sana/bosh harfli so'zlarni manba
matnida qidiradi. Aniqlanmagan holatlar (masalan faktda tekshiriladigan
token umuman yo'q) ehtiyotkorlik bilan "tasdiqlangan" deb hisoblanadi, chunki
ularni noto'g'ri "shubhali" deb belgilash foydalanuvchini chalg'itadi.
"""

from .rules.extractor import extract_checkable_tokens


def _normalize(text):
    return text.lower().replace("'", "'").replace("’", "'")


def annotate_key_facts(key_facts, source_text):
    """key_facts: [{"fact": str, "page": N}, ...] -> har biriga "verified" bool qo'shadi."""
    if not key_facts:
        return key_facts

    normalized_source = _normalize(source_text)
    annotated = []

    for item in key_facts:
        fact_text = item.get('fact', '') if isinstance(item, dict) else str(item)
        tokens = extract_checkable_tokens(fact_text)

        if not tokens:
            verified = True
        else:
            verified = all(_normalize(token) in normalized_source for token in tokens)

        annotated.append({**item, 'verified': verified})

    return annotated
