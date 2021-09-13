from typing import List, Set

from ....repository.translate import TranslationRepository
from .base import ApiKind

from ..types import ActionType, HttpMethodType
from ..http_status import HttpStatus, NotFound, OK, BadRequest, Conflict


class CustomPostActionApi(ApiKind):
    def __init__(self, action_name: str):
        self.action_name = action_name

    def http_status_list(self) -> List[HttpStatus]:
        return [
            OK(),
            BadRequest(),
            NotFound(),
            Conflict()
        ]

    def action_types(self) -> Set[ActionType]:
        return set()

    def method_type(self) -> HttpMethodType:
        return HttpMethodType.Post

    def rest_endpoint_extension(self) -> str:
        return self.endpoint_extension()

    def operation_word(self) -> str:
        return self.action_name

    def operation_word_en(self) -> str:
        return TranslationRepository.translate(self.action_name).lower()

    def endpoint_extension(self) -> str:
        return TranslationRepository.translate(self.action_name).lower()
