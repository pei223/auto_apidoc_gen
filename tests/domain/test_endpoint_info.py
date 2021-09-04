import pytest_mock

from app.domain.value_objects.api_kinds import AddApi, DeleteApi, ReadApi, SearchApi
from app.domain.value_objects.endpoint_info import EndpointInfo, aggregate_by_entity
from app.domain.value_objects.entity import Entity


def _mock_translation_repository(mocker: pytest_mock.MockFixture):
    def mock_func(text: str):
        d = {
            "サンプル1": "first_sample",
            "サンプル2": "second_sample"
        }
        return d[text]

    entity_mock = mocker.Mock(spec=Entity)
    entity_mock.endpoint_text = "aaaaaaaaa"
    mocker.patch("app.repository.translate.TranslationRepository.translate").side_effect = mock_func


def test_aggregate_by_entity():
    entities = [
        Entity("サンプル1"),
        Entity("サンプル2"),
        Entity("サンプル1"),
        Entity("サンプル2"),
        Entity("サンプル2"),
    ]
    api_nl_names = [
        "サンプル1一覧を取得する", "サンプル2一覧を取得する",
        "サンプル1を登録する", "サンプル2を削除する",
        "サンプル2を登録する"
    ]
    api_kinds = [
        ReadApi(),
        ReadApi(),
        AddApi(),
        DeleteApi(),
        AddApi()
    ]
    endpoints = aggregate_by_entity(entities=entities, api_kind_ls=api_kinds, api_nl_names=api_nl_names)
    assert endpoints[0].entity.entity_name == "サンプル1"
    assert len(endpoints[0].api_nl_names) == 2
    assert len(endpoints[0].api_kind_ls) == 2

    assert endpoints[1].entity.entity_name == "サンプル2"
    assert len(endpoints[1].api_nl_names) == 3
    assert len(endpoints[1].api_kind_ls) == 3


def test_generate_endpoint_urls(mocker: pytest_mock.MockFixture):
    _mock_translation_repository(mocker)

    entity1 = Entity("サンプル1")
    api_nl_names = [
        "サンプル1を登録する",
        "サンプル1一覧を取得する",
        "サンプル1を削除する",
        "サンプル1を検索する",
    ]
    api_kinds = [
        AddApi(),
        ReadApi(),
        DeleteApi(),
        SearchApi(),
    ]

    endpoint_info = EndpointInfo(entity=entity1, api_kind_ls=api_kinds, api_nl_names=api_nl_names)
    urls = endpoint_info.generate_endpoint_urls(True)

    assert urls[0] == "/first_samples/"
    assert urls[1] == "/first_samples/"
    assert urls[2] == "/first_samples/{id}"
    assert urls[3] == "/first_samples/search"
