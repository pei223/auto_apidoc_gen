from typing import Set, Optional

from . import (
    CustomPostActionApi,
    FindApi,
    AddApi,
    SearchApi,
    ReadApi,
    DeleteApi,
    UpdateApi,
    ApiKind,
)
from app.domain.value_objects.types import ActionType, ModifierType


def resolve_api_type(
    actions: Set[ActionType],
    modifier: Optional[ModifierType],
    custom_action_candidate: Optional[str],
) -> ApiKind:
    if custom_action_candidate:
        return CustomPostActionApi(custom_action_candidate)
    api_types = [
        FindApi(),
        AddApi(),
        UpdateApi(),
        SearchApi(),
        ReadApi(),
        UpdateApi(),
        DeleteApi(),
    ]
    for api_type in api_types:
        if actions == api_type.action_types():
            if not modifier or modifier == api_type.modifier_type():
                return api_type
    raise RuntimeError("ActionTypeが不正")
