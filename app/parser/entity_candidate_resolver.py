from tokenize import Token


def is_entity_candidate(token: Token) -> bool:
    if token.part_of_speech.split(",")[0] == "名詞":
        return True
    return False
