from abc import ABCMeta, abstractmethod
from typing import List, Set, Optional

from ..parameters import SchemaParamInfo, ParamInfo
from ..types import ActionType, ModifierType, HttpMethodType
from ..http_status import HttpStatus


class ApiKind(metaclass=ABCMeta):
    @abstractmethod
    def http_status_list(self) -> List[HttpStatus]:
        pass

    @abstractmethod
    def action_types(self) -> Set[ActionType]:
        pass

    @abstractmethod
    def endpoint_extension(self) -> str:
        pass

    @abstractmethod
    def operation_word(self) -> str:
        """
        操作を表す単語を返却
        :return:
        """
        pass

    @abstractmethod
    def operation_word_en(self) -> str:
        pass

    @abstractmethod
    def response_schema(self, entity_en_name: str) -> SchemaParamInfo:
        pass

    def modifier_type(self) -> Optional[ModifierType]:
        return None

    def method_type(self) -> HttpMethodType:
        return HttpMethodType.Get

    def rest_endpoint_extension(self) -> str:
        return ""

    def path_parameters(self) -> List[ParamInfo]:
        return []

    def query_parameters(self) -> List[ParamInfo]:
        return []

    def request_body(self, entity_en_name: str) -> Optional[SchemaParamInfo]:
        return None
