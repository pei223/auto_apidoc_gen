from abc import ABCMeta, abstractmethod


class HttpStatus(metaclass=ABCMeta):
    @abstractmethod
    def status_code(self) -> int:
        """
        HTTPステータスコード
        :return:
        """
        pass

    @abstractmethod
    def description(self, entity_name: str, operation_word: str):
        """
        HTTPステータスの説明
        :param entity_name:
        :param operation_word:
        :return:
        """
        pass

    def is_succeed_status(self):
        return 300 > self.status_code() >= 200


class OK(HttpStatus):
    def status_code(self) -> int:
        return 200

    def description(self, entity_name: str, operation_word: str):
        return f"{entity_name}{operation_word}成功"


class BadRequest(HttpStatus):
    def status_code(self) -> int:
        return 400

    def description(self, entity_name: str, operation_word: str):
        return "リクエスト不正"


class Unauthorized(HttpStatus):
    def status_code(self) -> int:
        return 401

    def description(self, entity_name: str, operation_word: str):
        return "認証エラー"


class NotFound(HttpStatus):
    def status_code(self) -> int:
        return 404

    def description(self, entity_name: str, operation_word: str):
        return f"{entity_name}データが存在しない"


class Conflict(HttpStatus):
    def status_code(self) -> int:
        return 409

    def description(self, entity_name: str, operation_word: str):
        return f"{entity_name}データが重複している"


class InternalServerError(HttpStatus):
    def status_code(self) -> int:
        return 500

    def description(self, entity_name: str, operation_word: str):
        return "内部サーバーエラー"
