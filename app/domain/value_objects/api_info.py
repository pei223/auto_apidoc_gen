from .api_kinds import ApiKind


class ApiInfo:
    def __init__(self, api_sentence: str, api_kind: ApiKind):
        self.api_sentence = api_sentence
        self.api_kind = api_kind
