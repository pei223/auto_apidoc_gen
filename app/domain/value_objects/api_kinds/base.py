from abc import ABCMeta, abstractmethod
from typing import List, Set, Optional

from ..types import ActionType, ModifierType, HttpMethodType
from ..http_status import HttpStatus


class ApiKind(metaclass=ABCMeta):
    @abstractmethod
    def http_status_list(self) -> List[HttpStatus]:
        pass

    @abstractmethod
    def action_types(self) -> Set[ActionType]:
        pass

    def modifier_type(self) -> Optional[ModifierType]:
        return None

    def method_type(self) -> HttpMethodType:
        return HttpMethodType.Get

    def rest_endpoint_extension(self) -> str:
        return ""

    @abstractmethod
    def endpoint_extension(self) -> str:
        pass
