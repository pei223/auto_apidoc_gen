from typing import Set

from .value_objects.types import ActionType, ModifierType


class ApiKindNotMatched(BaseException):
    def __init__(self, action_types: Set[ActionType], modifier_type: ModifierType):
        self.message = (
            f"一致するAPI種別が見つかりませんでした\nactions: {action_types}\nmodifier: {modifier_type}"
        )
        self.action_types = action_types
        self.modifier_type = modifier_type
        super().__init__(self.message)
