from typing import List, Set

from ....repository.translate import TranslationRepository
from .base import ApiKind

from ..types import ActionType, HttpMethodType
from ..http_status import HttpStatus, NotFound, OK, BadRequest


class CustomPostActionApi(ApiKind):
    def __init__(self, action_name: str):
        self.action_name = action_name
        self._action_translated = None

    def http_status_list(self) -> List[HttpStatus]:
        return [
            OK(),
            BadRequest(),
            NotFound(),
        ]

    def action_types(self) -> Set[ActionType]:
        return set()

    def method_type(self) -> HttpMethodType:
        return HttpMethodType.Post

    def rest_endpoint_extension(self) -> str:
        return self.endpoint_extension()

    def endpoint_extension(self) -> str:
        if self._action_translated:
            return self._action_translated
        self._action_translated = TranslationRepository.translate(self.action_name).lower()
        return self._action_translated
