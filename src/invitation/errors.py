from common.errors.base import AppError
from common.errors.type.error import ErrorObject


class InvitationError(AppError):
    """Base class for invitation-related errors."""

    def __init__(self, error: ErrorObject):
        super().__init__(
            payload={"message": error.message},
            code=f"invitation.{error.code}",
            status_code=error.status_code,
        )


class InvitationErrors:
    INVITATION_NOT_FOUND = ErrorObject(
        code="not_found",
        message="invitation not found",
        status_code=401,
    )

    ALREADY_INVITED = ErrorObject(
        code="already_invited",
        message="The invitation is already been sent",
        status_code=409,
    )
