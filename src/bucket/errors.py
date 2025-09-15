from common.errors.base import AppError
from common.errors.type.error import ErrorObject


class BucketError(AppError):
    """Base class for all custom Bucket errors."""

    def __init__(self, error: ErrorObject):
        super().__init__(
            payload={"message": error.message},
            code=f"bucket.{error.code}",
            status_code=error.status_code,
        )


class BucketErrors:
    UPLOAD_FAILED = ErrorObject(
        code="upload_failed",
        message="Something went wrong.",
        status_code=500,
    )
    DELETE_FAILED = ErrorObject(
        code="delete_failed",
        message="Something went wrong.",
        status_code=500,
    )
    PRESIGNED_URL_FAILED = ErrorObject(
        code="presigned_url_failed",
        message="Something went wrong.",
        status_code=500,
    )
