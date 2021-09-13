from typing import List, Set, Optional

from .base import ApiKind

from ..types import ActionType, ModifierType
from ..http_status import HttpStatus, OK


class ReadApi(ApiKind):
    def http_status_list(self) -> List[HttpStatus]:
        return [
            OK(),
        ]

    def action_types(self) -> Set[ActionType]:
        return {
            ActionType.Get,
        }

    def modifier_type(self) -> Optional[ModifierType]:
        return ModifierType.All_or_List

    def operation_word(self) -> str:
        return "取得"

    def operation_word_en(self) -> str:
        return "read"

    def endpoint_extension(self) -> str:
        return "list"
