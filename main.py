from app.domain.value_objects.endpoint_info import aggregate_by_entity
from app.domain.value_objects.setting import Setting
from app.parser.parser import parse
from app.writer.stoplight_format import StoplightStudioFormat

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

    entities = []
    api_types = []
    for text in text_ls:
        entity, api_type = parse(text)
        entities.append(entity)
        api_types.append(api_type)

    endpoints = aggregate_by_entity(text_ls, entities, api_types)

    setting = Setting(
        require_authorization=False,
        error_response_schema={},
        error_response_schema_example={},
        is_rest=True,
        server_url="http://localhost:3000",
        add_internal_error=False
    )
    for endpoint in endpoints:
        print(endpoint.to_string(is_REST=False))
        print("\n\n")
        f = StoplightStudioFormat(endpoint, setting)
        f.parse()
        f.output_yaml(endpoint.entity.entity_name + ".yaml")
