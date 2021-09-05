from typing import List, Dict, Optional
from janome.tokenizer import Token

from ..domain.value_objects.types import ActionType

CUSTOM_ACTION_LS = ["保存", "確定", "キャンセル", "予約"]

ACTION_TYPE_WORDS_DICT: Dict[ActionType, List[str]] = {
    ActionType.Get: ["取得"],
    ActionType.Add: ["登録", "追加"],
    ActionType.Update: ["更新", "アップデート"],
    ActionType.Delete: ["削除", "消去"],
    ActionType.Search: ["検索"],
    ActionType.Custom: CUSTOM_ACTION_LS,
}


def resolve_action_type(
    token: Token, next_token: Optional[Token]
) -> Optional[ActionType]:
    for key, value in ACTION_TYPE_WORDS_DICT.items():
        if token.node.surface in value:
            return key
    return None
