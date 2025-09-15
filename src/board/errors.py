from common.errors.base import AppError
from common.errors.type.error import ErrorObject


class BoardError(AppError):
    """Base class for board-related errors."""

    def __init__(self, error: ErrorObject):
        super().__init__(
            payload={"message": error.message},
            code=f"board.{error.code}",
            status_code=error.status_code,
        )


class BoardErrors:
    BOARD_NOT_FOUND = ErrorObject(
        code="not_found",
        message="Board not found",
        status_code=401,
    )
