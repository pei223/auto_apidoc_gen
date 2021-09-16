from pathlib import Path
from app.domain.value_objects.endpoint_info import aggregate_by_entity
from app.parser.parser import parse
from app.repository.translate import TranslationRepository
from app.utils.pyyaml_util import output_yaml
from app.writer.openapi_yaml.openapi_yaml_writer import OpenAPIYamlFormatWriter
from app.writer.openapi_yaml.openapi_setting import OpenAPIYamlSetting

if __name__ == "__main__":
    text_ls = [
        "店舗情報を取得する",
        "店舗情報の一覧を取得する",
        "店舗情報一覧を取得する",
        "お気に入り登録する",
        "予約状態を更新する",
        "予約状態を確定する",
        "予約状態を取得する",
        "店舗情報を検索する",
        "お気に入り削除する",
        "お気に入り一覧を取得する"
    ]

    setting = OpenAPIYamlSetting.from_file("sample_setting.json")
    TranslationRepository.inject_custom_translate_dict(setting.custom_translate_dict)

    entities = []
    api_types = []
    for text in text_ls:
        entity, api_type = parse(text)
        entities.append(entity)
        api_types.append(api_type)

    root = Path("./docs/reference")
    root.joinpath("common").mkdir(parents=True, exist_ok=True)
    root.joinpath("paths").mkdir(parents=True, exist_ok=True)

    endpoints = aggregate_by_entity(text_ls, entities, api_types)

    for endpoint in endpoints:
        print(endpoint.to_string(is_REST=False))
        print("\n\n")
        f = OpenAPIYamlFormatWriter(endpoint, setting)
        f.parse()
        output_yaml(f.get_tree(), str(root.joinpath("paths").joinpath(endpoint.entity.entity_nl_name + ".yaml")))

    setting.output_auth_model(str(root.joinpath("common").joinpath("Authorization.yaml")))
    setting.output_error_response_model(str(root.joinpath("common").joinpath("ErrorResponse.yaml")))
