from dataclasses import dataclass
import inflection as i
import re

from ...repository.translate import TranslationRepository

_EXCLUDE_WORD_ON_TRANSLATE_LIST = ["情報", "状態"]


@dataclass
class Entity:
    def __init__(self, entity_nl_name: str):
        self.entity_nl_name = entity_nl_name
        self._endpoint_name = None

    @property
    def entity_en_name(self):
        if not self._endpoint_name:
            extracted_entity_name = re.sub("|".join(_EXCLUDE_WORD_ON_TRANSLATE_LIST), "", self.entity_nl_name)
            translated_text = TranslationRepository.translate(extracted_entity_name)
            self._endpoint_name = self._words_to_endpoint(translated_text)
        return self._endpoint_name

    def _words_to_endpoint(self, translated_text: str):
        text_ls = translated_text.split()
        # ls = LS()
        norm_text_ls = []
        for text in text_ls:
            # normalized = ls.stem(text)
            # norm_text_ls.append(normalized)
            norm_text_ls.append(text)
        norm_text_ls[-1] = i.pluralize(norm_text_ls[-1])
        return "_".join(norm_text_ls).lower()

    def __eq__(self, other: "Entity"):
        if not isinstance(other, Entity):
            return False
        return self.entity_nl_name == other.entity_nl_name
