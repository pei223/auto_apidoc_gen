from dataclasses import dataclass
from typing import List
import nltk
from nltk.stem.lancaster import LancasterStemmer as LS
import inflection as i

from ...repository.translate import TranslationRepository


@dataclass
class Entity:
    def __init__(self, entity_name: str):
        self.entity_name = entity_name
        self._endpoint_text = None

    @property
    def endpoint_text(self):
        if not self._endpoint_text:
            translated_text = TranslationRepository().translate(self.entity_name)
            self._endpoint_text = self._words_to_endpoint(translated_text)
        return self._endpoint_text

    def _words_to_endpoint(self, translated_text: str):
        text_ls = translated_text.split()
        ls = LS()
        norm_text_ls = []
        for text in text_ls:
            # normalized = ls.stem(text)
            # norm_text_ls.append(normalized)
            norm_text_ls.append(text)
        norm_text_ls[-1] = i.pluralize(norm_text_ls[-1])
        return "_".join(norm_text_ls).lower()

    def __eq__(self, other: 'Entity'):
        if not isinstance(other, Entity):
            return False
        return self.entity_name == other.entity_name
