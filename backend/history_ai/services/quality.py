"""Mavzu sifati ro'yxati (checklist): admin har mavzuning qanchalik to'liqligini ko'radi.

`required` — asosiy talablar; qolganlari — darsni boyituvchi ixtiyoriy qismlar (oldindan sinash,
blok ichidagi savol, sabab-oqibat, xarita/rasm). Natija: har mavzu uchun belgilar ro'yxati va ball.
"""
from ..models import STATUS_DONE, GeneratedAsset, Lesson, Topic

MIN_TEST_QUESTIONS = 20


def _check(key, label, ok, required=True):
    return {'key': key, 'label': label, 'ok': bool(ok), 'required': required}


def topic_quality(topic, lesson, assets):
    plan = (lesson.lesson_plan if lesson else None) or {}
    quiz = (lesson.quiz if lesson else None) or {}
    blocks = plan.get('blocks') or []
    facts = plan.get('key_facts') or []
    test_qs = ((assets.get(GeneratedAsset.KIND_TOPIC_TEST) or {}).get('questions')) or []
    is_language = bool(plan.get('vocabulary'))

    checks = [
        _check('goals', "Kamida 2 ta o'quv maqsadi bor", len(plan.get('goals') or []) >= 2),
        _check('blocks', 'Kamida 3 ta matn bloki bor', len(blocks) >= 3),
        _check('facts', 'Kamida 3 ta asosiy fakt bor', len(facts) >= 3),
        _check('summary', 'Xulosa yozilgan', (plan.get('summary') or '').strip()),
        _check('test', f"Mavzu testida kamida {MIN_TEST_QUESTIONS} ta savol bor", len(test_qs) >= MIN_TEST_QUESTIONS),
        _check('quiz', 'Mini-viktorinada kamida 3 ta savol bor', len(quiz.get('questions') or []) >= 3),
    ]
    if not is_language:  # til kursida kitob beti va tarix o'yinlari yo'q
        sourced = bool(blocks) and all(b.get('pages') for b in blocks) and all(f.get('page') for f in facts)
        checks.append(_check('pages', "Har blok va faktga bet raqami ko'rsatilgan", sourced))
        for kind, label in (
            (GeneratedAsset.KIND_GAME_TIMELINE, "Xronologiya o'yini bor"),
            (GeneratedAsset.KIND_GAME_MATCHING, "Moslashtirish o'yini bor"),
            (GeneratedAsset.KIND_GAME_FILL_BLANK, "Bo'sh joyni to'ldirish o'yini bor"),
        ):
            checks.append(_check(kind, label, assets.get(kind)))
    checks += [
        _check('pretest', 'Oldindan sinash savollari bor', plan.get('pretest'), required=False),
        _check('block_checks', 'Bloklar ichida mini-savol bor', any(b.get('check') for b in blocks), required=False),
        _check('why', '"Nega?" (sabab-oqibat) bloki bor', plan.get('why'), required=False),
        _check('images', 'Xarita yoki rasm bor', plan.get('images') or plan.get('maps'), required=False),
        _check('takeaways', 'Asosiy fikrlar ("Katta rasm") bor', plan.get('takeaways'), required=False),
        _check('explanations', '"Nega?" izohlari savollarning kamida yarmida bor',
               test_qs and sum(bool(q.get('explanation')) for q in test_qs) * 2 >= len(test_qs), required=False),
        _check('levels', 'Test savollari darajalangan', test_qs and all(q.get('level') for q in test_qs), required=False),
    ]
    required = [c for c in checks if c['required']]
    optional = [c for c in checks if not c['required']]
    return {
        'topic_id': topic.id, 'title': topic.title, 'section': topic.section_id,
        'checks': checks,
        'required_ok': sum(c['ok'] for c in required), 'required_total': len(required),
        'bonus_ok': sum(c['ok'] for c in optional), 'bonus_total': len(optional),
    }


def book_quality(book):
    topics = list(Topic.objects.filter(book=book).order_by('order'))
    lessons = {l.topic_id: l for l in Lesson.objects.filter(topic__in=topics, status=STATUS_DONE)}
    assets = {}
    for a in GeneratedAsset.objects.filter(topic__in=topics, status=STATUS_DONE):
        assets.setdefault(a.topic_id, {})[a.kind] = a.data
    return [topic_quality(t, lessons.get(t.id), assets.get(t.id, {})) for t in topics]
