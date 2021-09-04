from dataclasses import dataclass


class RequireAuthorization:
    pass


class AddInternalErrorStatus:
    pass


class ErrorResponseInterface:
    pass


@dataclass
class Setting:
    require_authorization: bool
    error_response_interface: str
    add_internal_error: bool
    is_rest: bool
    server_url: str
