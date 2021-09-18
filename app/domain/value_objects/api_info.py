from .api_kinds import ApiKind


class ApiInfo:
    def __init__(self, api_sentence: str, api_wrap_up_sentence: str, api_kind: ApiKind):
        self.api_sentence = api_sentence
        self.api_wrap_up_sentence = api_wrap_up_sentence
        self.api_kind = api_kind
