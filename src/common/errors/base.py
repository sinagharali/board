from fastapi.responses import JSONResponse


class AppError(Exception):
    """Base class for all custom application errors."""

    def __init__(self, payload: dict, code: str, status_code: int = 400):
        self.payload = payload
        self.status_code = status_code
        self.code = code

    def __str__(self):
        return f"{self.code} ({self.status_code}): {self.payload.get('message')}"

    def to_response(self):
        return JSONResponse(
            status_code=self.status_code,
            content={"code": self.code, **self.payload},
        )


class ValidationError(AppError):
    def __init__(self, errors: list[list[dict]]):
        super().__init__(
            payload={"message": "Validation failed.", "details": errors},
            code="validation_error",
            status_code=400,
        )


class InternalError(AppError):
    def __init__(self):
        super().__init__(
            payload={"message": "Something went wrong."},
            code="something_went_wrong",
            status_code=500,
        )


class ImageValidationError(AppError):
    def __init__(
        self,
        message: str,
        code: str = "invalid_image",
        status_code: int = 400,
        **extra,
    ):
        payload = {"message": message, **extra}
        super().__init__(payload=payload, code=code, status_code=status_code)
