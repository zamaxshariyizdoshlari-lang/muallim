"""Kitob yakuniy imtihoni: barcha mavzularning to'liq test savollari birlashtiriladi."""

import random

from .rules.exceptions import NotEnoughDataError
from .topic_test_builder import build_topic_test


def build_book_exam(book, pages_by_topic):
    """pages_by_topic: {topic: [(page_number, text), ...]} -> {"questions": [...]}"""
    questions = []
    for topic, pages in pages_by_topic.items():
        try:
            for q in build_topic_test(topic, pages)['questions']:
                questions.append({**q, 'topic': topic.title})
        except NotEnoughDataError:
            continue

    if not questions:
        raise NotEnoughDataError(
            "Yakuniy imtihon uchun savollar topilmadi. Avval mavzular uchun dars rejasini yarating."
        )

    random.shuffle(questions)
    return {'questions': questions}
