from enum import Enum


class ActionType(Enum):
    Get = 0
    Add = 1
    Update = 2
    Delete = 3
    Search = 4
    Custom = 100


class ModifierType(Enum):
    All_or_List = 1
    Multi = 2
    Detail = 3


class HttpMethodType(Enum):
    Post = "POST"
    Get = "GET"
    Delete = "DELETE"
    Put = "PUT"
