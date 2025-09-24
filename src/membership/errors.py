from common.errors.base import AppError
from common.errors.type.error import ErrorObject


class MembershipError(AppError):
    """Base class for Membership-related errors."""

    def __init__(self, error: ErrorObject):
        super().__init__(
            payload={"message": error.message},
            code=f"membership.{error.code}",
            status_code=error.status_code,
        )


class MembershipErrors:
    ALREADY_MEMBER = ErrorObject(
        code="already_member",
        message="The end user is already member.",
        status_code=409,
    )
