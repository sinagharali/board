from common.errors.base import AppError
from common.errors.type.error import ErrorObject


class ACLError(AppError):
    """Base class for all custom Authorization Errors."""

    def __init__(self, error: ErrorObject):
        super().__init__(
            payload={"message": error.message},
            code=f"auth.{error.code}",
            status_code=error.status_code,
        )


class ACLErrors:
    ACTION_NOT_VALID = ErrorObject(
        code="action_not_valid",
        message="action is invalid",
        status_code=500,
    )
    UNATHORIZED_ACTION = ErrorObject(
        code="unathorized_action",
        message="Action is unathorized",
        status_code=403,
    )
    OPENFGA_FAILED = ErrorObject(
        code="opefga_failed",
        message="Openfga failed action",
        status_code=500,
    )
