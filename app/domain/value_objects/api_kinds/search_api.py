from typing import List, Set

from .base import ApiKind
from ..parameters import ParamInfo, ParamType, FirstObjectSchemaParam, ArraySchemaParam, ObjectSchemaParam, \
    ValueSchemaParam, SchemaParamInfo

from ..types import ActionType
from ..http_status import HttpStatus, OK, BadRequest


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

    def operation_word(self) -> str:
        return "検索"

    def operation_word_en(self) -> str:
        return "search"

    def query_parameters(self) -> List[ParamInfo]:
        return [ParamInfo(type=ParamType.String, name="q", required=True, description="検索条件"), ]

    def response_schema(self, entity_name: str) -> SchemaParamInfo:
        # NOTE ここentity名で自動化できるとかなりすごい
        return FirstObjectSchemaParam(properties=[
            ArraySchemaParam(
                name=entity_name,
                items=ObjectSchemaParam(name="", properties=[
                    ValueSchemaParam(name="id", type=ParamType.String),
                    ValueSchemaParam(name="name", type=ParamType.String),
                ])),
        ])
