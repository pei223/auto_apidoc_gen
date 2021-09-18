import pytest

from app.domain.value_objects.setting import SettingTypeError
from app.writer.openapi_yaml.openapi_setting import OpenAPIYamlSetting

correct_dict = {
    "authorization": {
        "required": True,
        "token_type": "bearer"
    },
    "error_response_model": {
        "title": "エラーレスポンス",
        "type": "object",
        "properties": {
            "errors": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string"
                        }
                    },
                    "required": [
                        "code"
                    ]
                }
            }
        },
        "required": [
            "errors"
        ]
    },
    "is_rest": True,
    "add_internal_error": False,
    "server_url": "http://localhost:3000",
    "custom_translate_dict": {
        "確定": "save"
    }
}


def test_setting_validation_with_invalid_authorization_type():
    with pytest.raises(SettingTypeError):
        OpenAPIYamlSetting.from_dict(
            {
                "authorization": bool,
                "error_response_model": {
                    "title": "エラーレスポンス",
                    "type": "object",
                    "properties": {
                        "errors": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "code": {
                                        "type": "string"
                                    }
                                },
                                "required": [
                                    "code"
                                ]
                            }
                        }
                    },
                    "required": [
                        "errors"
                    ]
                },
                "is_rest": True,
                "add_internal_error": False,
                "server_url": "http://localhost:3000",
                "custom_translate_dict": {
                    "確定": "save"
                }
            }
        )


def test_setting_validation_with_invalid_error_response_model_type():
    with pytest.raises(SettingTypeError):
        OpenAPIYamlSetting.from_dict(
            {
                "authorization": {
                    "required": True,
                    "token_type": "bearer"
                },
                "error_response_model": 12,
                "is_rest": True,
                "add_internal_error": False,
                "server_url": "http://localhost:3000",
                "custom_translate_dict": {
                    "確定": "save"
                }
            }
        )


def test_setting_validation_with_invalid_is_rest_type():
    with pytest.raises(SettingTypeError):
        OpenAPIYamlSetting.from_dict(
            {
                "authorization": {
                    "required": True,
                    "token_type": "bearer"
                },
                "error_response_model": {
                    "title": "エラーレスポンス",
                    "type": "object",
                    "properties": {
                        "errors": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "code": {
                                        "type": "string"
                                    }
                                },
                                "required": [
                                    "code"
                                ]
                            }
                        }
                    },
                    "required": [
                        "errors"
                    ]
                },
                "is_rest": "hogehoge",
                "add_internal_error": False,
                "server_url": "http://localhost:3000",
                "custom_translate_dict": {
                    "確定": "save"
                }
            }
        )


def test_setting_validation_with_invalid_add_internal_error_type():
    with pytest.raises(SettingTypeError):
        OpenAPIYamlSetting.from_dict(
            {
                "authorization": {
                    "required": True,
                    "token_type": "bearer"
                },
                "error_response_model": {
                    "title": "エラーレスポンス",
                    "type": "object",
                    "properties": {
                        "errors": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "code": {
                                        "type": "string"
                                    }
                                },
                                "required": [
                                    "code"
                                ]
                            }
                        }
                    },
                    "required": [
                        "errors"
                    ]
                },
                "is_rest": True,
                "add_internal_error": 1234.5,
                "server_url": "http://localhost:3000",
                "custom_translate_dict": {
                    "確定": "save"
                }
            }
        )


def test_setting_validation_with_invalid_server_url_type():
    with pytest.raises(SettingTypeError):
        OpenAPIYamlSetting.from_dict(
            {
                "authorization": {
                    "required": True,
                    "token_type": "bearer"
                },
                "error_response_model": {
                    "title": "エラーレスポンス",
                    "type": "object",
                    "properties": {
                        "errors": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "code": {
                                        "type": "string"
                                    }
                                },
                                "required": [
                                    "code"
                                ]
                            }
                        }
                    },
                    "required": [
                        "errors"
                    ]
                },
                "is_rest": True,
                "add_internal_error": False,
                "server_url": 1234,
                "custom_translate_dict": {
                    "確定": "save"
                }
            }
        )


def test_setting_validation_with_invalid_custom_translate_dict_type():
    with pytest.raises(SettingTypeError):
        OpenAPIYamlSetting.from_dict(
            {
                "authorization": {
                    "required": True,
                    "token_type": "bearer"
                },
                "error_response_model": {
                    "title": "エラーレスポンス",
                    "type": "object",
                    "properties": {
                        "errors": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "code": {
                                        "type": "string"
                                    }
                                },
                                "required": [
                                    "code"
                                ]
                            }
                        }
                    },
                    "required": [
                        "errors"
                    ]
                },
                "is_rest": True,
                "add_internal_error": False,
                "server_url": "http://localhost:3000",
                "custom_translate_dict": 12
            }
        )


def test_setting_validation_with_no_error():
    setting = OpenAPIYamlSetting.from_dict(correct_dict)
    assert setting is not None
