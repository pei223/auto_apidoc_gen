from collections import OrderedDict

from ...domain.value_objects.setting import Setting
from ...utils.pyyaml_util import output_yaml


class OpenAPIYamlSetting(Setting):
    def output_auth_model(self, filepath: str):
        auth_model = OrderedDict(
            {
                "openapi": "3.1.0",
                "info": {"title": "Authorization", "version": "1.0"},
                "servers": [{"url": self.server_url}],
                "paths": {},
                "components": {
                    "schemas": {},
                    "parameters": {
                        "bearer": {
                            "name": "Authorization",
                            "in": "header",
                            "required": True,
                            "schema": {"type": "string"},
                            "description": self.authorization_info["schema"],
                        }
                    },
                },
            }
        )
        output_yaml(auth_model, filepath)
