from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError

from common.errors.base import AppError


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_dict = {}

    for err in exc.errors():
        loc = err.get("loc")
        msg = err.get("msg")
        err_type = err.get("type")  # type of error (useful as code)

        # Clean the prefix for ValueError messages
        if isinstance(msg, str) and msg.lower().startswith("value error"):
            msg = msg.split(",", 1)[-1].strip()

        if loc and len(loc) >= 2 and loc[0] == "body":
            field = loc[1]
            # Include both code and message in details
            error_dict.setdefault(field, []).append({"code": err_type, "message": msg})

    # Wrap in AppError to unify response format
    app_error = AppError(
        payload={
            "message": "Validation failed.",
            "details": error_dict,
        },
        code="validation_error",
        status_code=422,
    )
    return await app_exception_handler(request, app_error)


async def app_exception_handler(request: Request, exc: AppError):
    return exc.to_response()


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(AppError, app_exception_handler)
