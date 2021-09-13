from collections import OrderedDict
from typing import Dict, List

from ..stoplight.response_writer import generate_response_schema
from ...domain.value_objects.api_kinds import ApiKind
from ...domain.value_objects.endpoint_info import EndpointInfo
from ...domain.value_objects.http_status import InternalServerError, Unauthorized, HttpStatus
from ...domain.value_objects.parameters import ParamInfo
from ...domain.value_objects.setting import Setting


class StoplightFormatWriter:
    def __init__(self, endpoint_info: EndpointInfo, setting: Setting):
        self._tree = OrderedDict({"openapi": "3.1.0", "info": {}, "servers": {}, "paths": {}})
        self._endpoint_info = endpoint_info
        self._endpoint_urls = self._endpoint_info.generate_endpoint_urls(setting.is_rest)
        self._setting = setting

    def parse(self):
        self._parse_basic_items()
        self._parse_each_endpoint()

    def _parse_basic_items(self):
        self._tree["servers"] = [
            {"url": self._setting.server_url},
        ]
        self._tree["info"] = {
            "title": self._endpoint_info.entity.entity_name + "API",
            "version": "1.0",
            "summary": self._endpoint_info.entity.entity_name + "関連API",
        }

    def _parse_each_endpoint(self):
        for order in range(self._endpoint_info.api_count()):
            api_nl_name = self._endpoint_info.api_nl_names[order]
            api_kind = self._endpoint_info.api_kind_ls[order]
            endpoint_url = self._endpoint_urls[order]
            if not self._tree["paths"].get(endpoint_url):
                self._tree["paths"][endpoint_url] = {}

            self._tree["paths"][endpoint_url].update({
                "parameters": self._get_path_parameters(api_kind),
                api_kind.method_type().value.lower(): {
                    **self._get_method_data(api_nl_name, api_kind),
                    **{"description": api_nl_name,
                       "operationId": f"{api_kind.operation_word_en()}-{self._endpoint_info.entity.endpoint_text}"}
                }
            })

    def _get_path_parameters(self, api_kind: ApiKind) -> List[Dict[str, any]]:
        def _gen_path_param_dict(path_param: ParamInfo):
            return {
                "schema": {"type": path_param.type.value},
                "name": path_param.name,
                "in": "path",
                "required": path_param.required,
                "description": path_param.description
            }

        return list(map(lambda path_param: _gen_path_param_dict(path_param), api_kind.path_parameters()))

    def _get_method_data(self, api_nl_name: str, api_kind: ApiKind) -> Dict[str, any]:
        return {
            "summary": api_nl_name,
            "tags": [],
            "responses": self._get_each_response_of_method(api_kind),
        }

    def _get_each_response_of_method(self, api_kind: ApiKind) -> Dict[str, any]:
        entity = self._endpoint_info.entity
        responses = {}
        http_status_list = api_kind.http_status_list()
        if self._setting.add_internal_error:
            http_status_list.append(InternalServerError())
        if self._setting.is_authorization_required():
            http_status_list.append(Unauthorized())

        for http_status in http_status_list:
            response_schema = generate_response_schema(api_kind.response_schema(
                entity_name=entity.entity_name)) if http_status.is_succeed_status() \
                else self._setting.error_response_schema.copy()
            responses[str(http_status.status_code())] = {
                "description": http_status.description(entity.entity_name, api_kind.operation_word()),
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
