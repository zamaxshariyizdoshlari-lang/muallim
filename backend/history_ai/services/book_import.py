"""Tayyor JSON (format_version 1) dan kitobni import qilish: AI ham, PDF ham kerak emas."""

import random

from django.db import transaction

from ..models import (
    STATUS_DONE, Book, BookExam, GeneratedAsset, Lesson, Section, SectionExam, Topic,
)

FORMAT_VERSION = 1
BOOK_EXAM_SIZE = 50
SECTION_EXAM_TARGET = 40


def _is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def _check_mcq(q, where, errors):
    if not isinstance(q, dict):
        errors.append(f"{where}: savol obyekt bo'lishi kerak")
        return
    if not str(q.get('question', '')).strip():
        errors.append(f"{where}: savol matni bo'sh")
    opts = q.get('options')
    if not isinstance(opts, list) or not 2 <= len(opts) <= 6 or not all(isinstance(o, str) and o.strip() for o in opts):
        errors.append(f"{where}: options 2-6 ta bo'sh bo'lmagan matn bo'lishi kerak")
    elif len(set(o.strip().lower() for o in opts)) != len(opts):
        errors.append(f"{where}: variantlar takrorlangan")
    ci = q.get('correct_index')
    if not _is_int(ci) or not isinstance(opts, list) or not 0 <= ci < len(opts):
        errors.append(f"{where}: correct_index variantlar oralig'ida emas")
    if not _is_int(q.get('page')):
        errors.append(f"{where}: page (bet raqami) butun son bo'lishi kerak")


def validate_book_json(data):
    """Xatolar ro'yxatini qaytaradi (bo'sh ro'yxat = hammasi to'g'ri)."""
    errors = []
    if not isinstance(data, dict) or data.get('format_version') != FORMAT_VERSION:
        return [f"format_version {FORMAT_VERSION} bo'lishi kerak"]

    book = data.get('book') or {}
    if not book.get('title') or not book.get('key'):
        errors.append("book.title va book.key majburiy")

    sections = data.get('sections')
    if not isinstance(sections, list) or not sections:
        return errors + ["sections bo'sh bo'lmagan ro'yxat bo'lishi kerak"]

    section_keys, topic_keys = set(), set()
    for si, sec in enumerate(sections):
        sw = f"sections[{si}]"
        if not sec.get('key') or not sec.get('title'):
            errors.append(f"{sw}: key va title majburiy")
        if sec.get('key') in section_keys:
            errors.append(f"{sw}: key takrorlangan ({sec.get('key')})")
        section_keys.add(sec.get('key'))
        if not sec.get('topics'):
            errors.append(f"{sw}: topics bo'sh")

        for ti, t in enumerate(sec.get('topics') or []):
            tw = f"{sw}.topics[{ti}] ({t.get('key')})"
            if not t.get('key') or not t.get('title'):
                errors.append(f"{tw}: key va title majburiy")
            if t.get('key') in topic_keys:
                errors.append(f"{tw}: key takrorlangan")
            topic_keys.add(t.get('key'))
            if not (_is_int(t.get('start_page')) and _is_int(t.get('end_page')) and t['start_page'] <= t['end_page']):
                errors.append(f"{tw}: start_page/end_page noto'g'ri")

            blocks = (t.get('explanation') or {}).get('blocks')
            if not blocks or not all(b.get('text') for b in blocks):
                errors.append(f"{tw}: explanation.blocks bo'sh yoki matnsiz blok bor")
            if not isinstance(t.get('test'), list) or len(t['test']) < 5:
                errors.append(f"{tw}: test kamida 5 ta savoldan iborat bo'lishi kerak")
            for qi, q in enumerate(t.get('test') or []):
                _check_mcq(q, f"{tw}.test[{qi}]", errors)

            games = t.get('games') or {}
            for qi, q in enumerate((games.get('fill_blank') or {}).get('questions', [])):
                _check_mcq(q, f"{tw}.games.fill_blank[{qi}]", errors)
            for qi, q in enumerate((t.get('practice') or {}).get('quiz', [])):
                _check_mcq(q, f"{tw}.practice.quiz[{qi}]", errors)
            for qi, q in enumerate((t.get('practice') or {}).get('book_questions', [])):
                if not q.get('question') or not q.get('answer'):
                    errors.append(f"{tw}.practice.book_questions[{qi}]: question va answer majburiy")
            items = (games.get('timeline') or {}).get('items')
            if items is not None and (len(items) < 2 or not all(i.get('label') for i in items)):
                errors.append(f"{tw}.games.timeline: kamida 2 ta label kerak")
            pairs = (games.get('matching') or {}).get('pairs')
            if pairs is not None:
                lefts = [p.get('left') for p in pairs]
                if len(pairs) < 2 or not all(p.get('left') and p.get('right') for p in pairs) or len(set(lefts)) != len(lefts):
                    errors.append(f"{tw}.games.matching: kamida 2 ta, chap tomon takrorlanmas bo'lishi kerak")
            slides = (t.get('presentation') or {}).get('slides')
            if slides is not None and not all(s.get('title') for s in slides):
                errors.append(f"{tw}.presentation: sarlavhasiz slayd bor")
    return errors


def _sample_exam(pool_by_topic, total, rng):
    """Mavzular bo'yicha navbatma-navbat (bir tekis) tasodifiy savol tanlaydi."""
    queues = {}
    for title, qs in pool_by_topic.items():
        qs = list(qs)
        rng.shuffle(qs)
        queues[title] = qs
    picked = []
    while len(picked) < total and any(queues.values()):
        for title in list(queues):
            if queues[title] and len(picked) < total:
                picked.append({**queues[title].pop(), 'topic': title})
    rng.shuffle(picked)
    return picked


@transaction.atomic
def import_book_json(data, user):
    errors = validate_book_json(data)
    if errors:
        raise ValueError(errors)

    bdata = data['book']
    book, created = Book.objects.get_or_create(
        key=bdata['key'], defaults={'title': bdata['title'], 'uploaded_by': user}
    )
    book.title = bdata['title']
    book.save()

    seen_sections, seen_topics = [], []
    order = 0
    counts = {'topics': 0, 'questions': 0}
    topic_tests = {}
    section_topic_titles = {}

    for si, sdata in enumerate(data['sections']):
        section, _ = Section.objects.update_or_create(
            book=book, key=sdata['key'], defaults={'title': sdata['title'], 'order': si + 1}
        )
        seen_sections.append(section.id)
        section_topic_titles[section.id] = []

        for t in sdata['topics']:
            order += 1
            topic, _ = Topic.objects.update_or_create(
                book=book, key=t['key'],
                defaults={
                    'section': section, 'title': t['title'], 'order': order,
                    'start_page': t['start_page'], 'end_page': t['end_page'],
                },
            )
            seen_topics.append(topic.id)
            section_topic_titles[section.id].append(topic)

            expl = t['explanation']
            Lesson.objects.update_or_create(
                topic=topic,
                defaults={
                    'created_by': user, 'status': STATUS_DONE, 'ai_provider': 'import', 'error_message': '',
                    'lesson_plan': {
                        'goals': expl.get('goals', []),
                        'blocks': expl['blocks'],
                        'key_facts': [{**f, 'verified': True} for f in expl.get('key_facts', [])],
                        'summary': expl.get('summary', ''),
                    },
                    'quiz': {
                        'questions': (t.get('practice') or {}).get('quiz', []),
                        'book_questions': (t.get('practice') or {}).get('book_questions', []),
                    },
                },
            )

            games = t.get('games') or {}
            payloads = {
                GeneratedAsset.KIND_PRESENTATION: t.get('presentation'),
                GeneratedAsset.KIND_GAME_TIMELINE: games.get('timeline'),
                GeneratedAsset.KIND_GAME_MATCHING: games.get('matching'),
                GeneratedAsset.KIND_GAME_FILL_BLANK: games.get('fill_blank'),
                GeneratedAsset.KIND_TOPIC_TEST: {'questions': t['test']},
            }
            for kind, payload in payloads.items():
                if payload:
                    GeneratedAsset.objects.update_or_create(
                        topic=topic, kind=kind,
                        defaults={
                            'created_by': user, 'status': STATUS_DONE, 'ai_provider': 'import',
                            'error_message': '', 'data': payload,
                        },
                    )
                else:
                    GeneratedAsset.objects.filter(topic=topic, kind=kind).delete()

            topic_tests[topic.title] = t['test']
            counts['topics'] += 1
            counts['questions'] += len(t['test'])

    # JSON'da yo'q (kalitli) mavzu/bo'limlar o'chiriladi: JSON - yagona manba.
    Topic.objects.filter(book=book).exclude(key='').exclude(id__in=seen_topics).delete()
    Section.objects.filter(book=book).exclude(id__in=seen_sections).delete()

    for section_id, topics in section_topic_titles.items():
        rng = random.Random(f"section-{book.key}-{section_id}")
        per = max(3, SECTION_EXAM_TARGET // max(1, len(topics)))
        pool = {t.title: topic_tests[t.title] for t in topics}
        questions = _sample_exam(pool, per * len(topics), rng)
        SectionExam.objects.update_or_create(section_id=section_id, defaults={'data': {'questions': questions}})

    rng = random.Random(f"book-{book.key}")
    BookExam.objects.update_or_create(
        book=book,
        defaults={
            'created_by': user, 'status': STATUS_DONE, 'error_message': '',
            'data': {'questions': _sample_exam(topic_tests, BOOK_EXAM_SIZE, rng)},
        },
    )

    return {'book_id': book.id, 'created': created, 'sections': len(data['sections']), **counts}
