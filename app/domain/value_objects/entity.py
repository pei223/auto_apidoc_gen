from dataclasses import dataclass
from typing import List

import inflection as i

from .api_info import ApiInfo
from ...repository.translate import TranslationRepository
from ...utils.text_util import round_text


@dataclass
class Entity:
    def __init__(self, entity_ja_name: str, api_info_ls: List[ApiInfo]):
        self.entity_ja_name = entity_ja_name
        self.api_info_ls = api_info_ls

    @property
    def entity_en_name(self):
        translated_text = TranslationRepository.translate(self.entity_ja_name)
        return self._words_to_endpoint(translated_text)

    def generate_endpoint_urls(self, is_rest: bool) -> List[str]:
        return list(
            map(
                lambda api_info: f"/{self.entity_en_name}/"
                f"{api_info.api_kind.rest_endpoint_extension() if is_rest else api_info.api_kind.endpoint_extension()}",
                self.api_info_ls,
            )
        )

    def generate_wrap_up_sentences(self) -> List[str]:
        return list(
            map(
                lambda api_info: f"{self.entity_ja_name}{api_info.api_kind.operation_word()}API",
                self.api_info_ls,
            )
        )

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

    def to_inline_string(self, is_rest=True):
        result_rows = []
        endpoint_urls = self.generate_endpoint_urls(is_rest)
        for ind in range(len(self.api_info_ls)):
            result_rows.append(
                f"{endpoint_urls[ind]}:{self.api_info_ls[ind].api_kind.method_type(is_rest).value}"
            )
        return f"{round_text(self.entity_ja_name, 8)}API: [{', '.join(result_rows)}]"
