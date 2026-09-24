from rest_framework.throttling import UserRateThrottle


class AIGenerationThrottle(UserRateThrottle):
    """AI/generatsiya endpointlari uchun oddiy chegara (settings.AI_RATE_LIMIT)."""

    scope = 'ai_generation'
