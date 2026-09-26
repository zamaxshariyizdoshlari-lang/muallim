"""Mavzu bo'yicha TO'LIQ test: AI-quiz (sabab-oqibat) + qoida asosidagi
barcha fakt savollari birlashtiriladi. Yangi AI chaqiruvi kerak emas -
Lesson allaqachon yaratilgan bo'lishi kerak.
"""

from ..models import Lesson
from .rules.exceptions import NotEnoughDataError
from .rules.fill_blank_builder import build_all_fact_questions

MIN_TOTAL_QUESTIONS = 3


def build_topic_test(topic, pages):
    questions = []

    try:
        lesson = topic.lesson
    except Lesson.DoesNotExist:
        lesson = None

    if lesson and lesson.status == 'done' and lesson.quiz and lesson.quiz.get('questions'):
        questions.extend(lesson.quiz['questions'])

    questions.extend(build_all_fact_questions(pages))

    if len(questions) < MIN_TOTAL_QUESTIONS:
        raise NotEnoughDataError(
            "Bu mavzu uchun to'liq test tuzish uchun yetarli ma'lumot yo'q "
            f"(topildi: {len(questions)}, kamida {MIN_TOTAL_QUESTIONS} kerak). "
            "Avval dars rejasini yarating."
        )

    return {'questions': questions}
