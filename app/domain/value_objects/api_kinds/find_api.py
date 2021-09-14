from typing import List, Set

from .base import ApiKind
from ..parameters import ParamInfo, ParamType, SchemaParamInfo, FirstObjectSchemaParam, ValueSchemaParam

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

    def response_schema(self, entity_name: str) -> SchemaParamInfo:
        # NOTE ここentity名で自動化できるとかなりすごい
        return FirstObjectSchemaParam(properties=[
            ValueSchemaParam(name="id", type=ParamType.String),
            ValueSchemaParam(name="name", type=ParamType.String),
        ])
