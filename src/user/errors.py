from common.errors.base import AppError
from common.errors.type.error import ErrorObject


class UserError(AppError):
    def __init__(self, error: ErrorObject):
        super().__init__(
            payload={
                "message": error.message,
            },
            code=f"user.{error.code}",
            status_code=error.status_code,
        )


class UserErrors:
    ALREADY_REGISTERED = ErrorObject(
        code="already_registered",
        message="provided email addressis already registered",
        status_code=409,
    )

    NOT_REGISTERED = ErrorObject(
        code="not_registered",
        message="User is not registered",
        status_code=404,
    )
