from collections import OrderedDict
from typing import List, Tuple
import tqdm

from janome.analyzer import Analyzer

# from janome.charfilter import RegexReplaceCharFilter
from janome.tokenfilter import POSStopFilter
from janome.tokenizer import Tokenizer, Token

from .action_type_resolver import resolve_action_type
from .modifier_type_resolver import resolve_modifier_type
from .entity_name_resolver import is_entity_candidate, arrange_entity_name
from ..domain.value_objects.api_info import ApiInfo
from ..domain.value_objects.types import ActionType
from ..domain.value_objects.api_kinds import ApiKind, api_kind_resolver
from ..domain.value_objects.entity import Entity
from ..utils.text_util import round_text


def parse_sentences(api_sentences: List[str], verbose=True) -> List[Entity]:
    api_list_dict = OrderedDict({})
    iter_data = tqdm.tqdm(api_sentences) if verbose else api_sentences

    for api_sentence in iter_data:
        if verbose:
            iter_data.set_description("[Parsing {:20s}]".format(round_text(api_sentence, 20)))
        entity_name, api_wrap_up_sentence, api_kind = parse_sentence(api_sentence)
        if not api_list_dict.get(entity_name):
            api_list_dict[entity_name] = [ApiInfo(api_sentence, api_wrap_up_sentence, api_kind), ]
            continue
        api_list_dict[entity_name].append(ApiInfo(api_sentence, api_wrap_up_sentence, api_kind))
    return list(map(lambda key_api_info: Entity(key_api_info[0], key_api_info[1]), api_list_dict.items()))


def parse_sentence(api_sentence: str) -> Tuple[str, str, ApiKind]:
    tokenizer = Tokenizer()
    char_filters = [
        # RegexReplaceCharFilter("", "")
    ]
    token_filters = [
        POSStopFilter(['記号', '接続詞', '副詞', '連体詞', "助詞", "助動詞", "感動詞"])
    ]
    analyzer = Analyzer(tokenizer=tokenizer, char_filters=char_filters, token_filters=token_filters)

    tokens: List[Token] = list(analyzer.analyze(api_sentence))

    entity_candidates: List[str] = []
    actions: List[ActionType] = []
    custom_action_candidate = None
    token_len = len(tokens)
    modifier = None
    # 後ろから探索する
    api_wrap_up_words = []
    for i, token in enumerate(tokens[::-1]):
        print("token", token)

        api_wrap_up_words.append(token.node.surface)

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
    # 逆から文章を解析しているためReverseする
    entity_name = arrange_entity_name(entity_candidates[::-1])
    api_type = api_kind_resolver.resolve_api_type(set(actions), modifier, custom_action_candidate)
    api_wrap_up_sentence = _arrange_api_wrap_up_sentence(api_wrap_up_words[::-1])
    # print(actions)
    return entity_name, api_wrap_up_sentence, api_type


def _arrange_api_wrap_up_sentence(api_words: List[str]):
    _exclude_on_wrap_up = ["する", "行う"]
    return "".join(filter(lambda word: word not in _exclude_on_wrap_up, api_words))
