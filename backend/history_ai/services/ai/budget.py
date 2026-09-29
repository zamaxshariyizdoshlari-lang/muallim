"""Oylik AI chaqiruvlar uchun umumiy (barcha o'qituvchilar bo'yicha) xarajat cheklovi.

Har bir foydalanuvchi soatiga 20 ta chaqiruv bilan cheklangan (AIGenerationThrottle), lekin bu
butun tizim uchun oylik xarajatni cheklamaydi - ko'p o'qituvchi hisobi yoki xato bitta hisobni
API xarajatini kutilmagan darajada oshirib yuborishi mumkin. Bu shunga qarshi so'nggi himoya.
"""
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone


class AIBudgetExceeded(Exception):
    """Oylik AI chaqiruvlar chegarasiga yetilganda ko'tariladi."""


def _cache_key():
    now = timezone.now()
    return f'ai_calls_{now.year}_{now.month:02d}'


def check_and_record_ai_call():
    """Chegara sozlanmagan bo'lsa (AI_MONTHLY_CALL_LIMIT=0) hech narsa qilmaydi.

    Limitga yetilgan bo'lsa AIBudgetExceeded ko'taradi (chaqiruvchi joyda try/except allaqachon
    bor - xabar Lesson/GeneratedAsset.error_message sifatida o'qituvchiga ko'rsatiladi).
    """
    limit = settings.AI_MONTHLY_CALL_LIMIT
    if not limit:
        return
    key = _cache_key()
    count = cache.get(key, 0)
    if count >= limit:
        raise AIBudgetExceeded(
            f"Oylik AI chaqiruvlar chegarasiga ({limit} ta) yetildi - xarajatni nazorat qilish "
            "uchun qo'yilgan. Keyingi oy boshida avtomatik tiklanadi (yoki AI_MONTHLY_CALL_LIMIT "
            "sozlamasini oshiring)."
        )
    try:
        cache.incr(key)
    except ValueError:
        cache.set(key, 1, timeout=60 * 60 * 24 * 32)
