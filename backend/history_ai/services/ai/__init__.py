from django.conf import settings

from .claude_provider import ClaudeProvider
from .gemini_provider import GeminiProvider


def get_ai_provider():
    """settings.AI_PROVIDER ('claude' yoki 'gemini') asosida provider qaytaradi."""
    provider = (settings.AI_PROVIDER or 'claude').lower()
    if provider == 'gemini':
        return GeminiProvider()
    return ClaudeProvider()
