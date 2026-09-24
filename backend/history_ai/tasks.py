import json
import re
import threading

from .models import STATUS_DONE, STATUS_FAILED, GeneratedAsset, Lesson
from .services.ai import get_ai_provider
from .services.fact_checker import annotate_key_facts
from .services.prompts import build_lesson_prompt, build_presentation_prompt
from .services.rules.exceptions import NotEnoughDataError
from .services.rules.fill_blank_builder import build_fill_blank
from .services.rules.matching_builder import build_matching
from .services.rules.timeline_builder import build_timeline

# AI orqali (fon oqimida, pullik/kvota chegarali) yaratiladigan turlar.
AI_ASSET_BUILDERS = {
    GeneratedAsset.KIND_PRESENTATION: build_presentation_prompt,
}

# Kod/qoida orqali (sinxron, bepul, tezkor) yaratiladigan turlar.
RULE_ASSET_BUILDERS = {
    GeneratedAsset.KIND_GAME_TIMELINE: build_timeline,
    GeneratedAsset.KIND_GAME_MATCHING: build_matching,
    GeneratedAsset.KIND_GAME_FILL_BLANK: build_fill_blank,
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
    source_text = '\n'.join(text for _, text in pages if text)

    try:
        provider = get_ai_provider()
        prompt = build_lesson_prompt(lesson.topic.title, pages)
        raw = provider.generate(prompt)
        data = _extract_json(raw)

        lesson_plan = data.get('lesson_plan')
        if lesson_plan and lesson_plan.get('key_facts'):
            lesson_plan['key_facts'] = annotate_key_facts(lesson_plan['key_facts'], source_text)

        lesson.lesson_plan = lesson_plan
        lesson.quiz = data.get('quiz')
        lesson.ai_provider = provider.name
        lesson.status = STATUS_DONE
        lesson.error_message = ''
        lesson.save()
    except Exception as exc:
        lesson.status = STATUS_FAILED
        lesson.error_message = str(exc)
        lesson.save()


def start_lesson_generation(lesson_id):
    """Lesson yaratishni fon oqimida (thread) boshlaydi, so'rovni bloklamaydi."""
    thread = threading.Thread(target=_run_lesson_generation, args=(lesson_id,), daemon=True)
    thread.start()


def _run_ai_asset_generation(asset_id):
    asset = GeneratedAsset.objects.get(id=asset_id)
    pages = _topic_pages(asset.topic)
    build_prompt = AI_ASSET_BUILDERS[asset.kind]

    try:
        provider = get_ai_provider()
        prompt = build_prompt(asset.topic.title, pages)
        raw = provider.generate(prompt)
        data = _extract_json(raw)

        asset.data = data
        asset.ai_provider = provider.name
        asset.status = STATUS_DONE
        asset.error_message = ''
        asset.save()
    except Exception as exc:
        asset.status = STATUS_FAILED
        asset.error_message = str(exc)
        asset.save()


def start_asset_generation(asset_id):
    """Asset turiga qarab: AI turlari fon oqimida, qoida asosidagilar darhol (sinxron)."""
    asset = GeneratedAsset.objects.get(id=asset_id)

    if asset.kind in RULE_ASSET_BUILDERS:
        pages = _topic_pages(asset.topic)
        build = RULE_ASSET_BUILDERS[asset.kind]
        try:
            asset.data = build(pages)
            asset.ai_provider = ''
            asset.status = STATUS_DONE
            asset.error_message = ''
        except NotEnoughDataError as exc:
            asset.status = STATUS_FAILED
            asset.error_message = str(exc)
        asset.save()
        return

    thread = threading.Thread(target=_run_ai_asset_generation, args=(asset_id,), daemon=True)
    thread.start()
