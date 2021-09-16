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
                        self.authorization_info.token_type: {
                            "name": "Authorization",
                            "in": "header",
                            "required": True,
                            "schema": {"type": "string"},
                            "description": f"{self.authorization_info.token_type} <token>",
                        }
                    },
                },
            }
        )
        output_yaml(auth_model, filepath)
