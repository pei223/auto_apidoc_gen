from typing import List, Set

from .base import ApiKind

from ..types import ActionType, ModifierType, HttpMethodType
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
