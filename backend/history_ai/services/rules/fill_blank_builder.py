import random

from .exceptions import NotEnoughDataError
from .extractor import extract_dated_events, extract_term_definitions

MIN_QUESTIONS = 3
MAX_QUESTIONS = 8
MAX_OPTIONS = 4


def _format_year(year):
    if year < 0:
        return f"miloddan avvalgi {abs(year)}-yil"
    return f"{year}-yil"


def _extract_facts(pages):
    """pages -> [{"question": str, "answer": str, "page": N}, ...] (sana + atamalar)."""
    facts = []

    for e in extract_dated_events(pages):
        answer = e['matched'] or _format_year(e['year'])
        blanked = e['text'].replace(e['matched'], '____', 1) if e['matched'] else e['text']
        facts.append({'question': blanked, 'answer': answer, 'page': e['page']})

    for t in extract_term_definitions(pages):
        facts.append({
            'question': f"{t['definition']} (Bu qanday atama?)",
            'answer': t['term'],
            'page': t['page'],
        })

    return facts


def _facts_to_questions(facts):
    """Har bir faktdan bir nechta noto'g'ri variant bilan savol quradi."""
    all_answers = [f['answer'] for f in facts]
    questions = []
    for fact in facts:
        pool = [a for a in all_answers if a != fact['answer']]
        distractors = random.sample(pool, k=min(MAX_OPTIONS - 1, len(pool)))
        options = distractors + [fact['answer']]
        random.shuffle(options)
        questions.append({
            'question': fact['question'],
            'options': options,
            'correct_index': options.index(fact['answer']),
            'page': fact['page'],
        })
    return questions


def build_fill_blank(pages):
    """"O'yin" sifatida o'ynaladigan qisqa (cheklangan) bo'sh joyni to'ldirish testi.

    AI ishlatilmaydi. Chiqish shakli QuizGame komponenti bilan bir xil:
    {"questions": [{"question", "options", "correct_index", "page"}, ...]}
    """
    facts = _extract_facts(pages)

    if len(facts) < MIN_QUESTIONS:
        raise NotEnoughDataError(
            "Bu mavzuda 'bo'sh joyni to'ldirish' testi uchun yetarli fakt topilmadi "
            f"(topildi: {len(facts)}, kamida {MIN_QUESTIONS} kerak)."
        )

    random.shuffle(facts)
    return {'questions': _facts_to_questions(facts[:MAX_QUESTIONS])}


def build_all_fact_questions(pages):
    """Mavzu bo'yicha TO'LIQ test uchun: matndan ajratilgan HAR BIR faktga bittadan
    savol - hech qanday cheklov yo'q (bir nechta o'nlab savol bo'lishi mumkin).
    """
    facts = _extract_facts(pages)
    if not facts:
        return []
    return _facts_to_questions(facts)
