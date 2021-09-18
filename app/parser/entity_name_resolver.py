from tokenize import Token
import re
from typing import List


def is_entity_candidate(token: Token) -> bool:
    if token.part_of_speech.split(",")[0] == "名詞":
        return True
    return False


def arrange_entity_name(entity_candidates: List[str]):
    exclude_words = ["情報", "状態", "詳細", "データ"]
    entity_name = "".join(entity_candidates)
    entity_name = re.sub("|".join(exclude_words), "", entity_name)
    return entity_name
