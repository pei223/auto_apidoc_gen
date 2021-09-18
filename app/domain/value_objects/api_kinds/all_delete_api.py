from typing import List, Set, Optional

from .base import ApiKind
from ..parameters import (
    ParamType,
    SchemaParamInfo,
    FirstObjectSchemaParam,
    ValueSchemaParam,
)

from ..types import ActionType, HttpMethodType, ModifierType
from ..http_status import HttpStatus, OK


class AllDeleteApi(ApiKind):
    def http_status_list(self) -> List[HttpStatus]:
        return [
            OK(),
        ]

    def action_types(self) -> Set[ActionType]:
        return {
            ActionType.Delete,
        }

    def modifier_type(self) -> Optional[ModifierType]:
        return ModifierType.All_or_List

    def method_type(self, is_rest: bool) -> HttpMethodType:
        return HttpMethodType.Delete if is_rest else HttpMethodType.Post

    def endpoint_extension(self) -> str:
        return "all_delete"

    def operation_word(self) -> str:
        return "全削除"

    def operation_word_en(self) -> str:
        return "all_delete"

    def response_schema(self, entity_en_name: str) -> SchemaParamInfo:
        return FirstObjectSchemaParam(
            properties=[ValueSchemaParam(name="result", type=ParamType.Boolean)]
        )
