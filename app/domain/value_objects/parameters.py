from dataclasses import dataclass
from enum import Enum


class ParamType(Enum):
    Integer = "integer"
    Number = "number"
    String = "string"
    Boolean = "boolean"


@dataclass
class ParamInfo:
    type: ParamType
    name: str
    required: bool
    description: str = ""

    def set_description(self, description: str):
        self.description = description
