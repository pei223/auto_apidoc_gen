from abc import ABCMeta, abstractmethod


class HttpStatus(metaclass=ABCMeta):
    @abstractmethod
    def status_code(self) -> int:
        """
        HTTPステータスコード
        :return:
        """
        pass

    def description(self):
        """
        HTTPステータスの説明
        :return:
        """
        return self.__class__.__name__


class OK(HttpStatus):
    def status_code(self) -> int:
        return 200


class BadRequest(HttpStatus):
    def status_code(self) -> int:
        return 400


class NotFound(HttpStatus):
    def status_code(self) -> int:
        return 404


class Conflict(HttpStatus):
    def status_code(self) -> int:
        return 409
