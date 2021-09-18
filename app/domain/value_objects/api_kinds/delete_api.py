from typing import List, Set

from .base import ApiKind
from ..parameters import (
    ParamInfo,
    ParamType,
    SchemaParamInfo,
    FirstObjectSchemaParam,
    ValueSchemaParam,
)

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

    def method_type(self, is_rest: bool) -> HttpMethodType:
        return HttpMethodType.Delete if is_rest else HttpMethodType.Post

    def rest_endpoint_extension(self) -> str:
        return "{id}"

    def endpoint_extension(self) -> str:
        return "{id}/delete"

    def operation_word(self) -> str:
        return "削除"

    def operation_word_en(self) -> str:
        return "delete"

    def path_parameters(self) -> List[ParamInfo]:
        return [
            ParamInfo(
                type=ParamType.Integer, name="id", required=True, description="id"
            )
        ]

    def response_schema(self, entity_en_name: str) -> SchemaParamInfo:
        return FirstObjectSchemaParam(
            properties=[ValueSchemaParam(name="result", type=ParamType.Boolean)]
        )
