from collections.abc import Iterable
from datetime import datetime
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ConfigDict, model_validator
from pydantic.alias_generators import to_camel

from common.errors.base import ValidationError
from common.validators.runner import run_validators


def datetime_to_str(dt: datetime) -> str:
    return dt.isoformat()


def uuid_to_str(id_: UUID):
    return str(id_)


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        serialize_by_alias=True,
        validate_by_name=True,
        json_encoders={datetime: datetime_to_str, UUID: uuid_to_str},
    )

    __validators__: dict[str, list] = {}

    @model_validator(mode="after")
    def validate_fields(cls, values):
        errors = {}
        for field, validators in cls.__validators__.items():
            value = getattr(values, field, None)
            field_errors = run_validators(value, validators, field)
            if field_errors:
                errors[field] = field_errors

        if errors:
            raise ValidationError(errors=errors)
        return values

    def serializable_dict(self, *, exclude_list: Iterable[str] | None = None, **kwargs):
        """
        Return a JSON-serializable dict representation of the model.

        Args:
            exclude_list: Iterable of field names to exclude from serialization.
            **kwargs: Additional keyword arguments passed to model_dump and jsonable_encoder.

        Returns:
            JSON-serializable dict with applied exclusions and encodings.

        """
        exclude = set(exclude_list) if exclude_list else set()
        default_dict = self.model_dump(exclude=exclude, **kwargs)
        return jsonable_encoder(default_dict, **kwargs)
