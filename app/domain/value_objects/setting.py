import json
from abc import abstractmethod, ABCMeta
from collections import OrderedDict
from dataclasses import dataclass
from typing import Dict, Optional

from .parameters import RefSchemaParam
from ...utils.pyyaml_util import output_yaml


@dataclass
class AuthorizationInfo:
    token_type: str
    required: bool

    @classmethod
    def from_dict(cls, data: Dict) -> 'AuthorizationInfo':
        token_type = data["token_type"]
        required = data["required"]
        return AuthorizationInfo(token_type, required)


@dataclass
class Setting(metaclass=ABCMeta):
    authorization_info: AuthorizationInfo
    error_response_schema: Dict[str, any]
    add_internal_error: bool
    is_rest: bool
    server_url: str
    custom_translate_dict: Dict[str, str]

    @classmethod
    def from_dict(cls, data: Dict) -> 'Setting':
        is_rest = data["is_rest"]
        error_res_schema = data.get("error_response_model") or {}
        add_internal_error = data["add_internal_error"]
        server_url = data["server_url"]
        custom_translate_dict = data["custom_translate_dict"] or {}
        auth_info = AuthorizationInfo.from_dict(data["authorization"])

        return cls(
            authorization_info=auth_info,
            error_response_schema=error_res_schema,
            is_rest=is_rest,
            add_internal_error=add_internal_error,
            server_url=server_url,
            custom_translate_dict=custom_translate_dict
        )

    @classmethod
    def from_file(cls, filepath: str) -> "Setting":
        with open(filepath, "r", encoding="utf8") as file:
            data: Dict = json.load(file, object_pairs_hook=OrderedDict)
            return cls.from_dict(data)

    def output_error_response_model(self, filepath: str):
        output_yaml(self.error_response_schema, filepath)

    @abstractmethod
    def output_auth_model(self, filepath: str):
        pass

    def is_authorization_required(self) -> bool:
        return self.authorization_info.required

    def error_response_ref_schema(self):
        return RefSchemaParam(name="error_response", ref_path="../common/ErrorResponse.yaml")

    def authorization_ref_schema(self):
        return RefSchemaParam(name="authorization_schema",
                              ref_path=f"../common/Authorization.yaml#/components/parameters/"
                                       f"{self.authorization_info.token_type}")
