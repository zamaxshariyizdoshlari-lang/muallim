import logging

from django.conf import settings

from .base import AIProvider

logger = logging.getLogger('history_ai.ai_usage')

DEFAULT_MODEL = 'claude-sonnet-5'


class ClaudeProvider(AIProvider):
    name = 'claude'

    def __init__(self):
        self._client = None

    @property
    def client(self):
        if self._client is None:
            import anthropic
            self._client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        return self._client

    def generate(self, prompt: str) -> str:
        message = self.client.messages.create(
            model=settings.AI_MODEL or DEFAULT_MODEL,
            max_tokens=4096,
            messages=[{'role': 'user', 'content': prompt}],
        )

        if message.usage:
            logger.info(
                'claude usage: input_tokens=%s output_tokens=%s',
                message.usage.input_tokens, message.usage.output_tokens,
            )

        return ''.join(
            block.text for block in message.content if getattr(block, 'type', None) == 'text'
        )
