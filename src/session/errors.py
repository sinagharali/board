from common.errors.base import AppError
from common.errors.type.error import ErrorObject


class SessionError(AppError):
    """Base class for session-related errors."""

    def __init__(self, error: ErrorObject):
        super().__init__(
            payload={"message": error.message},
            code=f"session.{error.code}",
            status_code=error.status_code,
        )


class SessionErrors:
    SESSION_NOT_FOUND = ErrorObject(
        code="not_found",
        message="Session not found",
        status_code=401,
    )
    MISS_MATCH_REFRESH_TOKEN = ErrorObject(
        code="miss_match_refresh_token",
        message="Refresh token missed match",
        status_code=401,
    )
    SESSION_EXPIRED = ErrorObject(
        code="expired",
        message="Session is expired",
        status_code=401,
    )
