from typing import List, Set

from .base import ApiKind
from ..parameters import ParamInfo, ParamType

from ..types import ActionType
from ..http_status import HttpStatus, NotFound, OK, BadRequest


class FindApi(ApiKind):
    def http_status_list(self) -> List[HttpStatus]:
        return [
            OK(),
            BadRequest(),
            NotFound(),
        ]

    def action_types(self) -> Set[ActionType]:
        return {
            ActionType.Get
        }

    def rest_endpoint_extension(self) -> str:
        return "{id}"

    def endpoint_extension(self) -> str:
        return "find/{id}"

    def operation_word(self) -> str:
        return "取得"

    def operation_word_en(self) -> str:
        return "find"

    def path_parameters(self) -> List[ParamInfo]:
        return [ParamInfo(type=ParamType.Integer, name="id", required=True, description="id")]
