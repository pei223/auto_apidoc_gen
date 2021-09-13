from typing import List, Set

from .base import ApiKind

from ..types import ActionType, HttpMethodType
from ..http_status import HttpStatus, OK, BadRequest


class AddApi(ApiKind):
    def http_status_list(self) -> List[HttpStatus]:
        return [
            OK(), BadRequest()
        ]

    def action_types(self) -> Set[ActionType]:
        return {
            ActionType.Add
        }

    def method_type(self) -> HttpMethodType:
        return HttpMethodType.Post

    def operation_word(self) -> str:
        return "登録"

    def operation_word_en(self) -> str:
        return "add"

    def endpoint_extension(self) -> str:
        return "add"
