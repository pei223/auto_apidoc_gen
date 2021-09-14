from typing import List, Set, Optional

from .base import ApiKind
from ..parameters import ParamInfo, ParamType, SchemaParamInfo, FirstObjectSchemaParam, ValueSchemaParam

from ..types import ActionType, HttpMethodType
from ..http_status import HttpStatus, NotFound, OK, BadRequest


class UpdateApi(ApiKind):
    def http_status_list(self) -> List[HttpStatus]:
        return [
            OK(),
            BadRequest(),
            NotFound(),
        ]

    def action_types(self) -> Set[ActionType]:
        return {
            ActionType.Update
        }

    def method_type(self) -> HttpMethodType:
        return HttpMethodType.Put

    def rest_endpoint_extension(self) -> str:
        return "{id}"

    def endpoint_extension(self) -> str:
        return "update/{id}"

    def operation_word(self) -> str:
        return "更新"

    def operation_word_en(self) -> str:
        return "update"

    def path_parameters(self) -> List[ParamInfo]:
        return [ParamInfo(type=ParamType.Integer, name="id", required=True, description="id")]

    def request_body(self, entity_en_name: str) -> Optional[SchemaParamInfo]:
        # NOTE ここentity名で自動化できるとかなりすごい
        return FirstObjectSchemaParam(properties=[
            ValueSchemaParam(name="name", type=ParamType.String)
        ])

    def response_schema(self, entity_en_name: str) -> SchemaParamInfo:
        return FirstObjectSchemaParam(properties=[
            ValueSchemaParam(name="result", type=ParamType.Boolean)
        ])
