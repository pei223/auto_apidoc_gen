from typing import List, Dict, Optional
from janome.tokenizer import Token

from ..domain.value_objects.types import ModifierType

MODIFIER_TYPE_WORDS_DICT: Dict[ModifierType, List[str]] = {
    ModifierType.All_or_List: ["全て", "全部", "全体", "一覧", "リスト"],
    ModifierType.Multi: [
        "複数",
    ],
}


def resolve_modifier_type(token: Token) -> Optional[ModifierType]:
    for key, value in MODIFIER_TYPE_WORDS_DICT.items():
        if token.node.surface in value:
            return key
    return None
