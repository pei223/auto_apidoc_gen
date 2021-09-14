from typing import List, Set, Optional

from .base import ApiKind
from ..parameters import SchemaParamInfo, FirstObjectSchemaParam, ValueSchemaParam, ParamType

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

    def request_body(self, entity_name: str) -> Optional[SchemaParamInfo]:
        # NOTE ここentity名で自動化できるとかなりすごい
        return FirstObjectSchemaParam(properties=[
            ValueSchemaParam(name="name", type=ParamType.String)
        ])

    def response_schema(self, entity_name: str) -> SchemaParamInfo:
        return FirstObjectSchemaParam(properties=[
            ValueSchemaParam(name="result", type=ParamType.Boolean)
        ])
