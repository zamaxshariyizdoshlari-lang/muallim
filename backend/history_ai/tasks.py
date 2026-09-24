import json
import re
import threading

from .models import Lesson
from .services.ai import get_ai_provider
from .services.prompts import build_lesson_prompt


def _extract_json(text):
    """AI ba'zan JSON atrofiga ```json qo'shishi mumkin — shuni tozalaydi."""
    text = text.strip()
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if not match:
        raise ValueError("AI javobida JSON topilmadi")
    return json.loads(match.group(0))


def _run_generation(lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    topic = lesson.topic
    pages = [(p.page_number, p.text) for p in topic.book.pages.filter(
        page_number__gte=topic.start_page, page_number__lte=topic.end_page
    )]

    try:
        provider = get_ai_provider()
        prompt = build_lesson_prompt(topic.title, pages)
        raw = provider.generate(prompt)
        data = _extract_json(raw)

        lesson.lesson_plan = data.get('lesson_plan')
        lesson.quiz = data.get('quiz')
        lesson.ai_provider = provider.name
        lesson.status = Lesson.STATUS_DONE
        lesson.save()
    except Exception as exc:
        lesson.status = Lesson.STATUS_FAILED
        lesson.error_message = str(exc)
        lesson.save()


def start_lesson_generation(lesson_id):
    """Lesson yaratishni fon oqimida (thread) boshlaydi, so'rovni bloklamaydi."""
    thread = threading.Thread(target=_run_generation, args=(lesson_id,), daemon=True)
    thread.start()
