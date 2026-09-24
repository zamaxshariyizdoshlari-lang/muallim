import re

# O'zbek tarix darsliklarida ko'p uchraydigan bob/paragraf sarlavha shakllari.
HEADING_PATTERNS = [
    re.compile(r'^\s*\d{1,3}[-\.]?\s*(bob|bo\'lim|bolim|mavzu|paragraf)\b', re.IGNORECASE),
    re.compile(r'^\s*[§]\s*\d{1,3}', re.IGNORECASE),
    re.compile(r'^\s*\d{1,3}[-\.]\s*§', re.IGNORECASE),
    re.compile(r'^\s*(I|II|III|IV|V|VI|VII|VIII|IX|X){1,4}\s*(bob|bo\'lim|bolim)\b', re.IGNORECASE),
]

MIN_HEADING_LEN = 4
MAX_HEADING_LEN = 120


def _looks_like_heading(line):
    line = line.strip()
    if not (MIN_HEADING_LEN <= len(line) <= MAX_HEADING_LEN):
        return False
    for pattern in HEADING_PATTERNS:
        if pattern.match(line):
            return True
    return False


def detect_topics(pages):
    """pages: [(page_number, text), ...] -> [{"title", "start_page", "end_page"}, ...]

    Oddiy evristika: har bir betning satrlarini ma'lum shakllar (masalan
    "3-bob", "§ 5", "II bob") bilan solishtirib, sarlavhalarni topadi.
    Sarlavha topilmasa, butun kitob bitta "Umumiy matn" mavzusi sifatida qaytariladi.
    """
    candidates = []
    for page_number, text in pages:
        if not text:
            continue
        for line in text.splitlines():
            if _looks_like_heading(line):
                candidates.append({'page': page_number, 'title': line.strip()})
                break

    if not candidates:
        last_page = pages[-1][0] if pages else 1
        first_page = pages[0][0] if pages else 1
        return [{
            'title': 'Umumiy matn',
            'start_page': first_page,
            'end_page': last_page,
        }]

    last_page_num = pages[-1][0]
    topics = []
    for i, cand in enumerate(candidates):
        start_page = cand['page']
        if i + 1 < len(candidates):
            next_start = candidates[i + 1]['page']
            end_page = max(start_page, next_start - 1)
        else:
            end_page = last_page_num
        topics.append({
            'title': cand['title'],
            'start_page': start_page,
            'end_page': end_page,
        })
    return topics
