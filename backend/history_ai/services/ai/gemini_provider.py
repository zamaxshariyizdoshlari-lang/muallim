import logging

from django.conf import settings

from .base import AIProvider

logger = logging.getLogger('history_ai.ai_usage')

DEFAULT_MODEL = 'gemini-3.5-flash-lite'


class GeminiQuotaError(Exception):
    """Gemini bepul kvotasi tugaganda yoki limitga urilganda ko'tariladi."""


class GeminiProvider(AIProvider):
    name = 'gemini'

    def __init__(self):
        self._client = None

    @property
    def client(self):
        if self._client is None:
            from google import genai
            self._client = genai.Client(api_key=settings.GEMINI_API_KEY)
        return self._client

    def generate(self, prompt: str) -> str:
        from google.genai.errors import ClientError

        model_name = settings.AI_MODEL or DEFAULT_MODEL

        try:
            response = self.client.models.generate_content(model=model_name, contents=prompt)
        except ClientError as exc:
            if exc.code == 429:
                raise GeminiQuotaError(
                    "Gemini bepul kvotasi tugadi. Birozdan keyin qayta urinib ko'ring "
                    "yoki .env faylida AI_PROVIDER=claude qilib zaxira provayderga o'ting."
                ) from exc
            raise

        usage = getattr(response, 'usage_metadata', None)
        if usage:
            logger.info(
                'gemini usage: prompt_tokens=%s output_tokens=%s total_tokens=%s',
                usage.prompt_token_count, usage.candidates_token_count, usage.total_token_count,
            )

        return response.text
