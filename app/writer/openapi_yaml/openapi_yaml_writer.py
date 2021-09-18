from collections import OrderedDict
from typing import Dict, List

from ..openapi_yaml.schema_writer import convert_openapi_schema
from ...domain.value_objects.api_info import ApiInfo
from ...domain.value_objects.api_kinds import ApiKind
from ...domain.value_objects.entity import Entity
from ...domain.value_objects.http_status import InternalServerError, Unauthorized
from ...domain.value_objects.parameters import ParamInfo
from ...domain.value_objects.setting import Setting


class OpenAPIYamlFormatWriter:
    def __init__(self, entity: Entity, setting: Setting):
        self._tree = OrderedDict({"openapi": "3.1.0", "info": {}, "servers": {}, "paths": {}})
        self._entity = entity
        self._endpoint_urls = self._entity.generate_endpoint_urls(setting.is_rest)
        self._setting = setting

    def parse(self):
        self._parse_basic_items()
        self._parse_each_endpoint()

    def _parse_basic_items(self):
        self._tree["servers"] = [
            {"url": self._setting.server_url},
        ]
        self._tree["info"] = {
            "title": self._entity.entity_ja_name + "API",
            "version": "1.0",
            "summary": self._entity.entity_ja_name + "関連API",
            "description": self._entity.entity_ja_name + "関連API"
        }

    def _parse_each_endpoint(self):
        for order in range(len(self._entity.api_info_ls)):
            api_info = self._entity.api_info_ls[order]
            endpoint_url = self._endpoint_urls[order]
            if not self._tree["paths"].get(endpoint_url):
                self._tree["paths"][endpoint_url] = {}

            self._tree["paths"][endpoint_url].update({
                "parameters": self._get_path_parameters(api_info.api_kind),
                api_info.api_kind.method_type(self._setting.is_rest).value.lower(): {
                    **self._get_method_data(api_info),
                    **{"description": api_info.api_sentence,
                       "operationId": f"{api_info.api_kind.operation_word_en()}-{self._entity.entity_en_name}"},
                    **{"parameters": self._get_query_parameters(api_info.api_kind) + self._get_header_parameters()}
                }
            })

    def _gen_param_dict(self, path_param: ParamInfo, param_kind: str):
        return {
            "schema": {"type": path_param.type.value},
            "name": path_param.name,
            "in": param_kind,
            "required": path_param.required,
            "description": path_param.description
        }

    def _get_path_parameters(self, api_kind: ApiKind) -> List[Dict[str, any]]:
        return list(map(lambda path_param: self._gen_param_dict(path_param, "path"), api_kind.path_parameters()))

    def _get_query_parameters(self, api_kind: ApiKind) -> List[Dict[str, any]]:
        return list(map(lambda path_param: self._gen_param_dict(path_param, "query"), api_kind.query_parameters()))

    def _get_header_parameters(self) -> List[Dict[str, any]]:
        return [convert_openapi_schema(self._setting.authorization_ref_schema()), ]

    def _get_method_data(self, api_info: ApiInfo) -> Dict[str, any]:
        method_data = {
            "summary": api_info.api_wrap_up_sentence + "API",
            "tags": [],
            "responses": self._get_each_response_of_method(api_info.api_kind),
        }
        request_body = api_info.api_kind.request_body(self._entity.entity_en_name)
        if request_body:
            method_data["requestBody"] = {
                "content": {
                    "application/json": {
                        "schema": convert_openapi_schema(request_body),
                        "examples": {},
                    }
                }
            }
        return method_data

    def _get_each_response_of_method(self, api_kind: ApiKind) -> Dict[str, any]:
        responses = {}
        http_status_list = api_kind.http_status_list()
        if self._setting.add_internal_error:
            http_status_list.append(InternalServerError())
        if self._setting.is_authorization_required():
            http_status_list.append(Unauthorized())

        for http_status in http_status_list:
            response_schema = convert_openapi_schema(api_kind.response_schema(
                entity_en_name=self._entity.entity_en_name)) if http_status.is_succeed_status() \
                else convert_openapi_schema(self._setting.error_response_ref_schema())
            responses[str(http_status.status_code())] = {
                "description": http_status.description(self._entity.entity_ja_name, api_kind.operation_word()),
                "content": {
                    "application/json": {
                        "schema": response_schema,
                        "examples": {},
                    }
                },
            }
        return responses

    def get_tree(self) -> Dict[str, any]:
        return self._tree
