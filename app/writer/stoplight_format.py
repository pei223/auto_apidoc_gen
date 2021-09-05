from collections import OrderedDict

import yaml
import codecs

from ..domain.value_objects.endpoint_info import EndpointInfo
from ..domain.value_objects.setting import Setting


class StoplightStudioFormat:
    def __init__(self, endpoint_info: EndpointInfo, setting: Setting):
        self._tree = OrderedDict(
            {"openapi": "3.1.0", "info": {}, "servers": {}, "paths": {}}
        )
        self._endpoint_info = endpoint_info
        self._endpoint_urls = self._endpoint_info.generate_endpoint_urls(
            setting.is_rest
        )
        self._setting = setting

    def parse(self):
        self._parse_basic_items()
        self._parse_each_api()

    def _parse_each_api(self):
        for i in range(self._endpoint_info.api_count()):
            self._parse_endpoint(i)

    def _parse_endpoint(self, order: int):
        endpoint_url = self._endpoint_urls[order]
        if not self._tree["paths"].get(endpoint_url):
            self._tree["paths"][endpoint_url] = {}
        self._set_path_parameters(order)
        self._set_each_method(order)

    def _set_path_parameters(self, order: int):
        api_kind = self._endpoint_info.api_kind_ls[order]
        endpoint_url = self._endpoint_urls[order]
        if not self._tree["paths"][endpoint_url].get("parameters"):
            self._tree["paths"][endpoint_url]["parameters"] = []
        if len(api_kind.path_parameters()) == 0:
            return
        dict_ls = []
        for path_param in api_kind.path_parameters():
            dict_ls.append(
                {
                    "schema": {"type": path_param.type.value},
                    "name": path_param.name,
                    "in": "path",
                    "required": path_param.required,
                }
            )
        self._tree["paths"][endpoint_url]["parameters"] = dict_ls

    def _set_each_method(self, order: int):
        api_kind = self._endpoint_info.api_kind_ls[order]
        endpoint_url = self._endpoint_urls[order]
        method_data = {
            "summary": self._endpoint_info.api_nl_names[order],
            "tags": [],
            "responses": self._get_each_response_of_method(order),
        }

        self._tree["paths"][endpoint_url][
            api_kind.method_type().value.lower()
        ] = method_data

    def _get_each_response_of_method(self, order: int):
        entity = self._endpoint_info.entity
        api_kind = self._endpoint_info.api_kind_ls[order]
        responses = {}
        for http_status in api_kind.http_status_list():
            if http_status.is_succeed_status():
                # TODO
                response_schema = {}
                response_examples = {}
            else:
                response_schema = {}
                response_examples = {}
            responses[str(http_status.status_code())] = {
                "description": http_status.description(
                    entity.entity_name, api_kind.operation_word()
                ),
                "content": {
                    "application/json": {
                        "schema": response_schema,
                        "examples": response_examples,
                    }
                },
            }
        return responses

    def _parse_basic_items(self):
        self._tree["servers"] = [
            {"url": self._setting.server_url},
        ]
        self._tree["info"] = {
            "title": self._endpoint_info.entity.entity_name + "API",
            "version": "1.0",
            "summary": self._endpoint_info.entity.entity_name + "関連API"
        }

    def output_yaml(self, filepath: str):
        self._adjust_ordereddict_to_yaml()
        with codecs.open(filepath, "w", "utf-8") as f:
            yaml.dump(self._tree, f, encoding="utf-8", allow_unicode=True)

    @staticmethod
    def _adjust_ordereddict_to_yaml():
        def represent_odict(dumper, instance):
            return dumper.represent_mapping("tag:yaml.org,2002:map", instance.items())

        yaml.add_representer(OrderedDict, represent_odict)

        def construct_odict(loader, node):
            return OrderedDict(loader.construct_pairs(node))

        yaml.add_constructor("tag:yaml.org,2002:map", construct_odict)
