from dataclasses import dataclass
from typing import List

from .api_kinds import ApiKind
from .entity import Entity


@dataclass
class EndpointInfo:
    api_nl_names: List[str]
    entity: Entity
    api_kind_ls: List[ApiKind]

    def generate_endpoint_urls(self, is_REST: bool) -> List[str]:
        return list(
            map(
                lambda api_kind: f"/{self.entity.endpoint_text}/"
                f"{api_kind.rest_endpoint_extension() if is_REST else api_kind.endpoint_extension()} ",
                self.api_kind_ls,
            )
        )

    def to_string(self, is_REST=True):
        result_rows = [
            self.entity.entity_name + "API list",
        ]
        endpoint_urls = self.generate_endpoint_urls(is_REST)
        for i in range(len(self.api_nl_names)):
            result_rows.append(
                f"\t{self.api_nl_names[i]}  ->  {endpoint_urls[i]} : {self.api_kind_ls[i].method_type().value}"
            )
        return "\n".join(result_rows)


def aggregate_by_entity(
    api_nl_names: List[str], entities: List[Entity], api_kind_ls: List[ApiKind]
) -> List[EndpointInfo]:
    """
    同一Entityごとに自然言語API名, API種別を集約する
    :param api_nl_names:
    :param entities:
    :param api_kind_ls:
    :return:
    """
    d = {}
    for api_nl_name, entity, api_kin in zip(api_nl_names, entities, api_kind_ls):
        if not d.get(entity.entity_name):
            d[entity.entity_name] = {
                "entity": entity,
                "api_kind_ls": [
                    api_kin,
                ],
                "api_nl_names": [
                    api_nl_name,
                ],
            }
            continue
        d[entity.entity_name]["api_kind_ls"].append(api_kin)
        d[entity.entity_name]["api_nl_names"].append(api_nl_name)

    endpoint_info_ls = []
    for key in d.keys():
        endpoint_info = EndpointInfo(
            entity=d[key]["entity"],
            api_nl_names=d[key]["api_nl_names"],
            api_kind_ls=d[key]["api_kind_ls"],
        )
        endpoint_info_ls.append(endpoint_info)
    return endpoint_info_ls
