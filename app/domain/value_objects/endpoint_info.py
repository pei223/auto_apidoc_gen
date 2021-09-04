from dataclasses import dataclass
from typing import List, Dict

from .api_kinds import ApiKind
from .entity import Entity


@dataclass
class EndpointInfo:
    entity: Entity
    api_kind: List[ApiKind]


def aggregate_by_entity(api_info_ls: List[ApiInfo]) -> Dict[Entity, ApiKind]:
    pass
