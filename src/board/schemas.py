from common.models.base_schema import BaseSchema
from common.validators.string import is_not_empty, max_length, min_length


class CreateBoardDto(BaseSchema):
    name: str
    caption: str | None

    __validators__ = {  # noqa: RUF012
        "name": [is_not_empty(), min_length(3), max_length(50)],
        "caption": [is_not_empty(), max_length(255)],
    }


class UpdateBoardDto(BaseSchema):
    name: str | None
    caption: str | None
