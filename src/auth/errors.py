from common.errors.base import AppError
from common.errors.type.error import ErrorObject


class AuthError(AppError):
    """Base class for all custom Authentication Errors."""

    def __init__(self, error: ErrorObject):
        super().__init__(
            payload={"message": error.message},
            code=f"auth.{error.code}",
            status_code=error.status_code,
        )


class AuthErrors:
    TOKEN_MISSING = ErrorObject(
        code="token_missing",
        message="Token is missing",
        status_code=401,
    )
    EXPIRED_SIGNATURE = ErrorObject(
        code="expired_signature",
        message="Token is expired",
        status_code=401,
    )
    INVALID_TOKEN = ErrorObject(
        code="invalid_token",
        message="Token is invalid",
        status_code=401,
    )
    MISMATCH_TOKEN_TYPE = ErrorObject(
        code="mismatch_token_type",
        message="Token type mismatch",
        status_code=401,
    )
    AUTH_HEADER_MISSING = ErrorObject(
        code="auth_header_missing",
        message="Authorization Header missing",
        status_code=403,
    )
