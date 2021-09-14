from typing import Dict
from googletrans import Translator


class _TranslationRepository:
    def __init__(self):
        self._translator = Translator()
        self._custom_translate_dict = {}
        self._memory_cache: Dict[str, str] = {}

    def translate(self, text: str):
        data_from_custom_dict = self._custom_translate_dict.get(text)
        if data_from_custom_dict:
            return data_from_custom_dict
        cached_data = self._memory_cache.get(text)
        if cached_data:
            return cached_data
        result = self._translator.translate(text).text
        self._memory_cache[text] = result
        return result

    def inject_custom_translate_dict(self, custom_dict: Dict[str, str]):
        self._custom_translate_dict = custom_dict


TranslationRepository = _TranslationRepository()
