from abc import ABC, abstractmethod


class AIProvider(ABC):
    """Barcha AI provayderlar shu interfeysni amalga oshiradi.

    Claude/Gemini almashtirilganda qolgan kod (views, tasks) o'zgarmaydi.
    """

    name = 'base'

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Berilgan promptga javob matnini qaytaradi."""
        raise NotImplementedError
