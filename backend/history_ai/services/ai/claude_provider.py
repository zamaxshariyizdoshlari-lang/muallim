from django.conf import settings

from .base import AIProvider


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
            model=settings.ANTHROPIC_MODEL,
            max_tokens=4096,
            messages=[{'role': 'user', 'content': prompt}],
        )
        return ''.join(
            block.text for block in message.content if getattr(block, 'type', None) == 'text'
        )
