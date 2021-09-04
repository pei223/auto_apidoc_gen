from typing import Dict
from googletrans import Translator

from ..utils.annotations import singleton_class


@singleton_class
class TranslationRepository:
    def __init__(self):
        self._translator = Translator()
        self._memory_cache: Dict[str, str] = {}

    def translate(self, text: str):
        cached_data = self._memory_cache.get(text)
        if cached_data:
            return cached_data
        result = self._translator.translate(text).text
        self._memory_cache[text] = result
        return result
