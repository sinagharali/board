from collections.abc import Iterable
from datetime import datetime
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from pydantic import ConfigDict
from pydantic.alias_generators import to_camel
from sqlmodel import SQLModel


def datetime_to_str(dt: datetime) -> str:
    return dt.isoformat()


def uuid_to_str(id_: UUID):
    return str(id_)


class BaseORM(SQLModel):
    model_config = ConfigDict(
        from_attributes=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
        alias_generator=to_camel,
        arbitrary_types_allowed=True,
        json_encoders={datetime: datetime_to_str, UUID: uuid_to_str},
    )

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
        default_dict = self.model_dump(exclude=exclude, exclude_unset=False, **kwargs)
        return jsonable_encoder(default_dict, **kwargs)
