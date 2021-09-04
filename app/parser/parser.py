from typing import List, Tuple

from janome.analyzer import Analyzer
from janome.charfilter import RegexReplaceCharFilter
from janome.tokenizer import Tokenizer, Token

from .action_type_resolver import resolve_action_type
from .modifier_type_resolver import resolve_modifier_type
from .entity_candidate_resolver import is_entity_candidate
from ..domain.value_objects.types import ActionType
from ..domain.value_objects.api_kinds import ApiKind, api_kind_resolver
from ..domain.value_objects.entity import Entity


def parse(text: str) -> Tuple[Entity, ApiKind]:
    tokenizer = Tokenizer()
    char_filters = [RegexReplaceCharFilter("情報|状態", "")]
    analyzer = Analyzer(tokenizer=tokenizer, char_filters=char_filters)

    tokens: List[Token] = list(analyzer.analyze(text))

    entity_candidates: List[str] = []
    actions: List[ActionType] = []
    custom_action_candidate = None
    token_len = len(tokens)
    modifier = None
    # 後ろから探索する
    for i, token in enumerate(tokens[::-1]):
        # print("token", token)

        _modifier = resolve_modifier_type(token)
        if _modifier:
            modifier = _modifier
            continue

        action = resolve_action_type(token, tokens[i + 1] if i < token_len - 1 else None)
        if action:
            if action != ActionType.Custom:
                actions.append(action)
                continue
            if len(actions) == 0:
                custom_action_candidate = token.node.surface
                actions.append(action)
                continue

        if is_entity_candidate(token):
            entity_candidates.append(token.node.surface)

    # print(actions, modifier, custom_action_candidate)
    entity = Entity("".join(entity_candidates))
    api_type = api_kind_resolver.resolve_api_type(set(actions), modifier, custom_action_candidate)
    # print(actions)
    return entity, api_type
