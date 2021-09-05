from typing import List, Set

from .base import ApiKind
from ..parameters import ParamInfo, ParamType

from ..types import ActionType, HttpMethodType
from ..http_status import HttpStatus, NotFound, OK, BadRequest


class DeleteApi(ApiKind):
    def http_status_list(self) -> List[HttpStatus]:
        return [
            OK(),
            BadRequest(),
            NotFound(),
        ]

    def action_types(self) -> Set[ActionType]:
        return {
            ActionType.Delete,
        }

    def method_type(self) -> HttpMethodType:
        return HttpMethodType.Delete

    def rest_endpoint_extension(self) -> str:
        return "{id}"

    def endpoint_extension(self) -> str:
        return "delete/{id}"

    def path_parameters(self) -> List[ParamInfo]:
        return [ParamInfo(type=ParamType.Integer, name="id", required=True)]
