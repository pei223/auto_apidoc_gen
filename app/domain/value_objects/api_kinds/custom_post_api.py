from typing import List, Set, Optional

from ..parameters import SchemaParamInfo, FirstObjectSchemaParam, ValueSchemaParam, ParamType
from ....repository.translate import TranslationRepository
from .base import ApiKind

from ..types import ActionType, HttpMethodType
from ..http_status import HttpStatus, NotFound, OK, BadRequest, Conflict


class CustomPostActionApi(ApiKind):
    def __init__(self, action_name: str):
        self.action_name = action_name

    def http_status_list(self) -> List[HttpStatus]:
        return [
            OK(),
            BadRequest(),
            NotFound(),
            Conflict()
        ]

    def action_types(self) -> Set[ActionType]:
        return set()

    def method_type(self) -> HttpMethodType:
        return HttpMethodType.Post

    def rest_endpoint_extension(self) -> str:
        return self.endpoint_extension()

    def operation_word(self) -> str:
        return self.action_name

    def operation_word_en(self) -> str:
        return TranslationRepository.translate(self.action_name).lower()

    def endpoint_extension(self) -> str:
        return TranslationRepository.translate(self.action_name).lower()

    def request_body(self, entity_en_name: str) -> Optional[SchemaParamInfo]:
        # NOTE ここentity名で自動化できるとかなりすごい
        return FirstObjectSchemaParam(properties=[
            ValueSchemaParam(name="name", type=ParamType.String)
        ])

    def response_schema(self, entity_en_name: str) -> SchemaParamInfo:
        return FirstObjectSchemaParam(properties=[
            ValueSchemaParam(name="result", type=ParamType.Boolean)
        ])
