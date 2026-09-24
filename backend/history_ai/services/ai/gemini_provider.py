from django.conf import settings

from .base import AIProvider


class GeminiProvider(AIProvider):
    name = 'gemini'

    def __init__(self):
        self._model = None

    @property
    def model(self):
        if self._model is None:
            import google.generativeai as genai
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self._model = genai.GenerativeModel(settings.GEMINI_MODEL)
        return self._model

    def generate(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text
