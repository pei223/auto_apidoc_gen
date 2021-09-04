from typing import List, Set

from .base import ApiKind

from ..types import ActionType, ModifierType, HttpMethodType
from ..http_status import HttpStatus, NotFound, OK, BadRequest


class SearchApi(ApiKind):
    def http_status_list(self) -> List[HttpStatus]:
        return [
            OK(),
            BadRequest(),
        ]

    def action_types(self) -> Set[ActionType]:
        return {
            ActionType.Search
        }

    def rest_endpoint_extension(self) -> str:
        return "search"

    def endpoint_extension(self) -> str:
        return "search"
