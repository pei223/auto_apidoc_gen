from typing import List

import yaml

from app.domain.value_objects.api_kinds import ApiKind
from app.domain.value_objects.endpoint_info import EndpointInfo
from app.domain.value_objects.setting import Setting


class StoplightStudioFormat:
    def __init__(self, endpoint_info: EndpointInfo, setting: Setting):
        self._tree = {
            "openapi": "3.1.0",
            "info": {},
            "servers": {},
            "paths": {}
        }
        self._endpoint_info = endpoint_info
        self._setting = setting

    def parse(self):
        self._tree["servers"]["url"] = self._setting.server_url

    def _parse_each_endpoints(self):
        endpoint_urls = self._endpoint_info.generate_endpoint_urls(self._setting.is_rest)
        for endpoint_url, api_kind in zip(endpoint_urls, self._endpoint_info.api_kind_ls):
            pass

    def _parse_endpoint(self, endpoint_url: str, api_kind: ApiKind):
        if not self._tree["paths"].get(endpoint_url):
            self._tree["paths"][endpoint_url] = {}
        if not self._tree["paths"][endpoint_url]["parameters"]
            pass

    def _parse_basic_items(self):
        self._tree["servers"]["url"] = self._setting.server_url
        self._tree["info"]["title"] = self._endpoint_info.entity.entity_name + "API"

    def output_yaml(self) -> str:
        return yaml.dump(self._tree)
