import json
from abc import abstractmethod, ABCMeta
from collections import OrderedDict
from dataclasses import dataclass
from typing import Dict

from .parameters import RefSchemaParam
from ...utils.pyyaml_util import output_yaml


class SettingParseError(BaseException):
    def __init__(self, message: str):
        self.message = message


class SettingKeyError(SettingParseError):
    def __init__(self, var_name: str, type_name: str):
        super().__init__(f"{var_name}に{type_name}の値を設定してください")


class SettingTypeError(SettingParseError):
    def __init__(self, var_name: str, type_name: str):
        super().__init__(f"{var_name}は{type_name}型である必要があります")


@dataclass
class AuthorizationInfo:
    token_type: str
    required: bool

    @classmethod
    def from_dict(cls, data: Dict) -> "AuthorizationInfo":
        type_dict = {"token_type": "string", "required": "bool"}
        try:
            token_type = data["token_type"]
            required = data["required"]
            if not isinstance(token_type, str):
                raise SettingTypeError(
                    "authorization/token_type", type_dict["token_type"]
                )
            if not isinstance(required, bool):
                raise SettingTypeError("authorization/required", type_dict["required"])
            return AuthorizationInfo(token_type, required)
        except KeyError as e:
            key = e.args[0]
            raise SettingKeyError(key, type_dict[key])


@dataclass
class Setting(metaclass=ABCMeta):
    authorization_info: AuthorizationInfo
    error_response_schema: Dict[str, any]
    add_internal_error: bool
    is_rest: bool
    server_url: str
    custom_translate_dict: Dict[str, str]

    @classmethod
    def from_dict(cls, data: Dict) -> "Setting":
        type_dict = {
            "is_rest": "bool",
            "error_response_model": "Object",
            "add_internal_error": "bool",
            "server_url": "string",
            "custom_translate_dict": "Object",
            "authorization": "Object",
        }
        try:
            is_rest = data["is_rest"]
            error_res_schema = data["error_response_model"]
            add_internal_error = data["add_internal_error"]
            server_url = data["server_url"]
            custom_translate_dict = data["custom_translate_dict"]
            auth_info = data["authorization"]

            if not isinstance(is_rest, bool):
                raise SettingTypeError("is_rest", type_dict["is_rest"])
            if not isinstance(error_res_schema, Dict):
                raise SettingTypeError(
                    "error_response_model", type_dict["error_response_model"]
                )
            if not isinstance(add_internal_error, bool):
                raise SettingTypeError(
                    "add_internal_error", type_dict["add_internal_error"]
                )
            if not isinstance(server_url, str):
                raise SettingTypeError("server_url", type_dict["server_url"])
            if not isinstance(custom_translate_dict, dict):
                raise SettingTypeError(
                    "custom_translate_dict", type_dict["custom_translate_dict"]
                )
            if not isinstance(auth_info, dict):
                raise SettingTypeError("authorization", type_dict["authorization"])

            return cls(
                authorization_info=AuthorizationInfo.from_dict(auth_info),
                error_response_schema=error_res_schema,
                is_rest=is_rest,
                add_internal_error=add_internal_error,
                server_url=server_url,
                custom_translate_dict=custom_translate_dict,
            )
        except KeyError as e:
            key = e.args[0]
            raise SettingKeyError(key, type_dict[key])

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
        return RefSchemaParam(
            name="error_response", ref_path="../common/ErrorResponse.yaml"
        )

    def authorization_ref_schema(self):
        return RefSchemaParam(
            name="authorization_schema",
            ref_path=f"../common/Authorization.yaml#/components/parameters/"
            f"{self.authorization_info.token_type}",
        )
