from typing import List, Set

from .base import ApiKind
from ..parameters import ParamInfo, ParamType

from ..types import ActionType
from ..http_status import HttpStatus, OK, BadRequest


class SearchApi(ApiKind):
    def http_status_list(self) -> List[HttpStatus]:
        return [
            OK(),
            BadRequest(),
        ]

    def action_types(self) -> Set[ActionType]:
        return {ActionType.Search}

    def rest_endpoint_extension(self) -> str:
        return "search"

    def endpoint_extension(self) -> str:
        return "search"

    def query_parameters(self) -> List[ParamInfo]:
        return [ParamInfo(type=ParamType.String, name="q", required=True, description="検索条件")]
