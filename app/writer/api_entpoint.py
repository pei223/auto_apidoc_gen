from ..domain.value_objects.api_kinds.base import ApiKind
from ..domain.value_objects.entity import Entity


def gen_api_endpoint(entity: Entity, api_type: ApiKind, is_REST: bool) -> str:
    return f"/{entity.endpoint_text}/{api_type.rest_endpoint_extension() if is_REST else api_type.endpoint_extension()}"
