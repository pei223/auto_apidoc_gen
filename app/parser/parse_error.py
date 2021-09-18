class ActionNotFound(BaseException):
    def __init__(self, api_sentence: str):
        self.message = f"APIのアクションが見つかりません: {api_sentence}"
        super().__init__(self.message)
        self.api_sentence = api_sentence


class EntityNotFound(BaseException):
    def __init__(self, api_sentence: str):
        self.message = f"APIのEntityが見つかりません: {api_sentence}"
        super().__init__(self.message)
        self.api_sentence = api_sentence
