import json
from abc import abstractmethod, ABCMeta
from collections import OrderedDict
from dataclasses import dataclass
from typing import Dict, Optional

from ...utils.pyyaml_util import output_yaml


@dataclass
class Setting(metaclass=ABCMeta):
    require_authorization: bool
    authorization_info: Optional[Dict[str, any]]
    error_response_schema: Dict[str, any]
    add_internal_error: bool
    is_rest: bool
    server_url: str

    @classmethod
    def from_file(cls, filepath: str) -> "Setting":
        with open(filepath, "r", encoding="utf8") as file:
            data: Dict = json.load(file, object_pairs_hook=OrderedDict)
            require_authorization = data["require_authorization"]
            is_rest = data["is_rest"]
            authorization = data.get("authorization") or None
            error_res_schema = data.get("error_response") or {}
            add_internal_error = data["add_internal_error"]
            server_url = data["server_url"]
            return cls(
                require_authorization=require_authorization,
                authorization_info=authorization,
                error_response_schema=error_res_schema,
                is_rest=is_rest,
                add_internal_error=add_internal_error,
                server_url=server_url,
            )

    def output_error_response_model(self, filepath: str):
        output_yaml(self.error_response_schema, filepath)

    @abstractmethod
    def output_auth_model(self, filepath: str):
        pass

    def is_authorization_required(self) -> bool:
        return self.require_authorization is not None
