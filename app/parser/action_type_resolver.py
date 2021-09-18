from typing import List, Dict, Optional
from janome.tokenizer import Token

from ..domain.value_objects.types import ActionType

ACTION_TYPE_WORDS_DICT: Dict[ActionType, List[str]] = {
    ActionType.Get: ["取得"],
    ActionType.Add: ["登録", "追加"],
    ActionType.Update: ["更新", "アップデート"],
    ActionType.Delete: ["削除", "消去"],
    ActionType.Search: ["検索"],
}


def resolve_action_type(
    token: Token, next_token: Optional[Token]
) -> Optional[ActionType]:
    for key, value in ACTION_TYPE_WORDS_DICT.items():
        if token.node.surface in value:
            return key
    if token.part_of_speech.split(",")[1] == "サ変接続":
        return ActionType.Custom
    return None
