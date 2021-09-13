from abc import ABCMeta, abstractmethod
from typing import List, Set, Optional

from ..parameters import SchemaParamInfo, ParamInfo, ObjectSchemaParam, ValueSchemaParam, ArraySchemaParam, \
    ParamType
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

    def response_schema(self, entity_name: str) -> SchemaParamInfo:
        # TODO デバッグコード
        v = ObjectSchemaParam(
            name="schema",
            properties=[
                ValueSchemaParam(name="test", type=ParamType.String),
                # RefSchemaParam(name="err", ref_path="aaaa.html"),
                ArraySchemaParam(
                    name="arr",
                    items=ObjectSchemaParam(
                        name="eee", properties=[ValueSchemaParam(name="aaa", type=ParamType.String)]
                    ),
                ),
            ],
        )
        return v
