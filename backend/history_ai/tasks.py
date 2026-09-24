import json
import re
import threading

from .models import STATUS_DONE, STATUS_FAILED, GeneratedAsset, Lesson
from .services.ai import get_ai_provider
from .services.prompts import (
    build_lesson_prompt,
    build_matching_game_prompt,
    build_presentation_prompt,
    build_timeline_game_prompt,
)

ASSET_PROMPT_BUILDERS = {
    GeneratedAsset.KIND_PRESENTATION: build_presentation_prompt,
    GeneratedAsset.KIND_GAME_TIMELINE: build_timeline_game_prompt,
    GeneratedAsset.KIND_GAME_MATCHING: build_matching_game_prompt,
}


def _extract_json(text):
    """AI ba'zan JSON atrofiga ```json qo'shishi mumkin — shuni tozalaydi."""
    text = text.strip()
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if not match:
        raise ValueError("AI javobida JSON topilmadi")
    return json.loads(match.group(0))


def _topic_pages(topic):
    return [
        (p.page_number, p.text)
        for p in topic.book.pages.filter(
            page_number__gte=topic.start_page, page_number__lte=topic.end_page
        )
    ]


def _run_lesson_generation(lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    pages = _topic_pages(lesson.topic)

    try:
        provider = get_ai_provider()
        prompt = build_lesson_prompt(lesson.topic.title, pages)
        raw = provider.generate(prompt)
        data = _extract_json(raw)

        lesson.lesson_plan = data.get('lesson_plan')
        lesson.quiz = data.get('quiz')
        lesson.ai_provider = provider.name
        lesson.status = STATUS_DONE
        lesson.save()
    except Exception as exc:
        lesson.status = STATUS_FAILED
        lesson.error_message = str(exc)
        lesson.save()


def start_lesson_generation(lesson_id):
    """Lesson yaratishni fon oqimida (thread) boshlaydi, so'rovni bloklamaydi."""
    thread = threading.Thread(target=_run_lesson_generation, args=(lesson_id,), daemon=True)
    thread.start()


def _run_asset_generation(asset_id):
    asset = GeneratedAsset.objects.get(id=asset_id)
    pages = _topic_pages(asset.topic)
    build_prompt = ASSET_PROMPT_BUILDERS[asset.kind]

    try:
        provider = get_ai_provider()
        prompt = build_prompt(asset.topic.title, pages)
        raw = provider.generate(prompt)
        data = _extract_json(raw)

        asset.data = data
        asset.ai_provider = provider.name
        asset.status = STATUS_DONE
        asset.save()
    except Exception as exc:
        asset.status = STATUS_FAILED
        asset.error_message = str(exc)
        asset.save()


def start_asset_generation(asset_id):
    """Taqdimot/o'yin yaratishni fon oqimida boshlaydi, so'rovni bloklamaydi."""
    thread = threading.Thread(target=_run_asset_generation, args=(asset_id,), daemon=True)
    thread.start()
