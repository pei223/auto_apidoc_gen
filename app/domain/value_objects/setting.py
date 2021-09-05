from dataclasses import dataclass
from typing import Dict


class RequireAuthorization:
    pass


class AddInternalErrorStatus:
    pass


class ErrorResponseInterface:
    pass


@dataclass
class Setting:
    require_authorization: bool
    error_response_schema: Dict
    error_response_schema_example: Dict
    add_internal_error: bool
    is_rest: bool
    server_url: str
