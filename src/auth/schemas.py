from typing import ClassVar

from common.models.base_schema import BaseSchema
from common.validators.email import validate_email
from common.validators.password import validate_password
from common.validators.string import is_not_empty, min_length


class SignupDto(BaseSchema):
    name: str
    email: str
    password: str

    __validators__ = {  # noqa: RUF012
        "name": [is_not_empty(), min_length(3)],
        "email": [is_not_empty(), validate_email()],
        "password": [is_not_empty(), validate_password()],
    }

    model_config: ClassVar[dict[str, str]] = {"extra": "forbid"}


class SigninDto(BaseSchema):
    email: str
    password: str

    __validators__ = {  # noqa: RUF012
        "email": [is_not_empty(), validate_email()],
        "password": [is_not_empty(), validate_password()],
    }

    model_config: ClassVar[dict[str, str]] = {"extra": "forbid"}
