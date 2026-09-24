"""Darslik matnidan sana, atama-ta'rif kabi faktlarni REGEX/QOIDA orqali ajratish.

AI ishlatilmaydi — shuning uchun natija sifat jihatidan haqiqiy NLP/NER'dan past
bo'lishi mumkin (masalan ba'zi ismlarni o'tkazib yuborishi yoki gap boshidagi
so'zni noto'g'ri "atama" deb tanlashi mumkin). Bu arzonlik uchun ongli kelishuv.
"""

import re

_ROMAN_VALUES = [
    ('M', 1000), ('CM', 900), ('D', 500), ('CD', 400),
    ('C', 100), ('XC', 90), ('L', 50), ('XL', 40),
    ('X', 10), ('IX', 9), ('V', 5), ('IV', 4), ('I', 1),
]


def _roman_to_int(roman):
    roman = roman.upper()
    value = 0
    i = 0
    for symbol, amount in _ROMAN_VALUES:
        while roman[i:i + len(symbol)] == symbol:
            value += amount
            i += len(symbol)
    return value if i == len(roman) else None


_YEAR_NUMERIC_RE = re.compile(
    r'(miloddan\s+avvalgi\s+)?(\d{1,4})\s*-?\s*yil(?:lar)?', re.IGNORECASE
)
_CENTURY_ROMAN_RE = re.compile(
    r'(miloddan\s+avvalgi\s+)?\b([IVXLCDM]{1,7})\s*asr', re.IGNORECASE
)

_SENTENCE_SPLIT_RE = re.compile(r'(?<=[.!?])\s+|\n+')

# Gap boshida tez-tez uchraydigan, "atama" sifatida noto'g'ri ushlanishi mumkin bo'lgan so'zlar.
_STOPWORDS = {
    'Bu', 'Shu', 'Ular', 'U', 'Biz', 'Ammo', 'Lekin', 'Va', 'Shuningdek',
    'Natijada', 'Keyin', 'Shunday', 'Ushbu', 'Har', 'Ba\'zi', 'Ko\'p',
}


def split_sentences(text):
    return [s.strip() for s in _SENTENCE_SPLIT_RE.split(text) if s.strip()]


def extract_dated_events(pages):
    """pages: [(page_number, text), ...] -> [{"year": int, "text": gap, "page": N}, ...]

    "year" — solishtirish uchun sonli qiymat (miloddan avvalgi bo'lsa manfiy).
    Xronologik tartibda (o'sish bo'yicha) qaytaradi, takrorlanganlarni olib tashlaydi.
    """
    events = []
    seen_texts = set()

    for page_number, text in pages:
        if not text:
            continue
        for sentence in split_sentences(text):
            year = None
            matched = None

            m = _YEAR_NUMERIC_RE.search(sentence)
            if m:
                value = int(m.group(2))
                year = -value if m.group(1) else value
                matched = m.group(0)
            else:
                m = _CENTURY_ROMAN_RE.search(sentence)
                if m:
                    century = _roman_to_int(m.group(2))
                    if century:
                        value = century * 100
                        year = -value if m.group(1) else value
                        matched = m.group(0)

            if year is None:
                continue

            normalized = sentence.strip()
            if normalized in seen_texts or len(normalized) < 5:
                continue
            seen_texts.add(normalized)
            events.append({'year': year, 'text': normalized, 'page': page_number, 'matched': matched})

    events.sort(key=lambda e: e['year'])
    return events


# "Atama — ta'rif" yoki "Atama - ta'rif" ko'rinishidagi qator (darsliklarda tez-tez uchraydi).
_WORD_CHARS = r"[A-Za-zʻʼ']+"
_TERM_DEFINITION_RE = re.compile(
    rf"^([A-Z]{_WORD_CHARS}(?:\s+{_WORD_CHARS}){{0,3}})\s*[—–\-]\s+(.{{8,}})$"
)


def extract_term_definitions(pages):
    """pages -> [{"term": str, "definition": str, "page": N}, ...]

    Faqat "Atama — ta'rif" shaklidagi qatorlarni topadi. Bu ko'p darsliklarda
    ishlatiladigan konvensiya, lekin har doim ham bunday yozilmasligi mumkin.
    """
    results = []
    seen_terms = set()

    for page_number, text in pages:
        if not text:
            continue
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            m = _TERM_DEFINITION_RE.match(line)
            if not m:
                continue
            term, definition = m.group(1).strip(), m.group(2).strip()
            if term in _STOPWORDS or term.lower() in seen_terms:
                continue
            if len(term) < 2 or len(definition) < 8:
                continue
            seen_terms.add(term.lower())
            results.append({'term': term, 'definition': definition, 'page': page_number})

    return results


_CAPITALIZED_WORD_RE = re.compile(r"\b[A-Z][A-Za-zʻʼ']{2,}\b")


def extract_checkable_tokens(text):
    """Ixtiyoriy matndan (masalan AI javobidan) tekshirilishi mumkin bo'lgan
    sana va bosh harfli so'zlarni (ism/joy nomzodlari) ajratadi.

    Fakt tekshiruvi uchun ishlatiladi — natija darslik manba matnida ham
    borligini solishtirish uchun.
    """
    tokens = set()

    for m in _YEAR_NUMERIC_RE.finditer(text):
        tokens.add(m.group(0).strip())
    for m in _CENTURY_ROMAN_RE.finditer(text):
        tokens.add(m.group(0).strip())
    for m in _CAPITALIZED_WORD_RE.finditer(text):
        word = m.group(0)
        if word not in _STOPWORDS:
            tokens.add(word)

    return tokens
