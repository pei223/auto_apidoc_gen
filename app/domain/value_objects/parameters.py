from enum import Enum
from abc import abstractmethod
from dataclasses import dataclass
from typing import List


class ParamType(Enum):
    Integer = "integer"
    Number = "number"
    String = "string"
    Boolean = "boolean"


@dataclass
class QueryParamInfo:
    name: str
    type: ParamType
    description: str
    required: bool = True


@dataclass
class PathParamInfo:
    name: str
    type: ParamType
    required: bool = True


class SchemaParamInfo:
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def to_string(self, indent: int = 0) -> str:
        pass


@dataclass
class ValueSchemaParam(SchemaParamInfo):
    name: str
    type: ParamType
    required: bool = True

    def to_string(self, indent: int = 0):
        prefix = "\t" * indent
        return f"{prefix}{self.name}: {self.type.value}"


@dataclass
class FirstObjectSchemaParam(SchemaParamInfo):
    properties: List[SchemaParamInfo]
    name: str = "schema"
    required: bool = True

    def to_string(self, indent: int = 0):
        result = ""
        prefix = "\t" * indent
        for param_info in self.properties:
            result += f"{param_info.to_string(indent + 1)}\n"
        return f"{prefix}{{\n{result}\n{prefix}}}"


@dataclass
class ObjectSchemaParam(SchemaParamInfo):
    name: str
    properties: List[SchemaParamInfo]
    required: bool = True

    def to_string(self, indent: int = 0):
        result = ""
        prefix = "\t" * indent
        for param_info in self.properties:
            result += f"{param_info.to_string(indent + 1)}\n"
        return f"{prefix}{self.name}: {{\n{result}\n{prefix}}}"


@dataclass
class ArraySchemaParam(SchemaParamInfo):
    name: str
    items: SchemaParamInfo
    required: bool = True

    def to_string(self, indent: int = 0) -> str:
        prefix = "\t" * indent
        return f"{prefix}{self.name}: [\n{self.items.to_string(indent + 1)}\n{prefix}]"


@dataclass
class RefSchemaParam(SchemaParamInfo):
    name: str
    ref_path: str
    required: bool = True

    def to_string(self, indent: int = 0) -> str:
        prefix = "\t" * indent
        return f"{prefix}{self.name}: {self.ref_path}"
