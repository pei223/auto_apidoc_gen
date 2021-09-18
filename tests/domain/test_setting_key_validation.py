import pytest

from app.domain.value_objects.setting import SettingKeyError
from app.writer.openapi_yaml.openapi_setting import OpenAPIYamlSetting


def test_setting_validation_without_authorization():
    with pytest.raises(SettingKeyError):
        OpenAPIYamlSetting.from_dict(
            {
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


def test_setting_validation_without_error_response_model():
    with pytest.raises(SettingKeyError):
        OpenAPIYamlSetting.from_dict(
            {
                "authorization": {
                    "required": True,
                    "token_type": "bearer"
                },
                "is_rest": True,
                "add_internal_error": False,
                "server_url": "http://localhost:3000",
                "custom_translate_dict": {
                    "確定": "save"
                }
            }
        )


def test_setting_validation_without_is_rest():
    with pytest.raises(SettingKeyError):
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
                "add_internal_error": False,
                "server_url": "http://localhost:3000",
                "custom_translate_dict": {
                    "確定": "save"
                }
            }
        )


def test_setting_validation_without_add_internal_error():
    with pytest.raises(SettingKeyError):
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
                "server_url": "http://localhost:3000",
                "custom_translate_dict": {
                    "確定": "save"
                }
            }
        )


def test_setting_validation_without_server_url():
    with pytest.raises(SettingKeyError):
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
                "custom_translate_dict": {
                    "確定": "save"
                }
            }
        )


def test_setting_validation_without_custom_translate_dict():
    with pytest.raises(SettingKeyError):
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
            }
        )


def test_setting_validation_with_no_error():
    setting = OpenAPIYamlSetting.from_dict({
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
    })
    assert setting is not None
