from datetime import datetime
from uuid import UUID

from sqlalchemy import Column, DateTime
from sqlmodel import Field

from common.models.base_orm_model import BaseORM


class Session(BaseORM, table=True):
    """
    Represents a login session for a user on a specific device.

    Fields:
    - **id**    : Primary key (UUID)
    - **user_id**       : Foreign key to User table (UUID)
    - **user_agent**    : User agent string of the client (str)
    - **refresh_token** : Hashed Refresh Token (str)
    - **created_at**    : Timestamp when the session was created (Datetime)
    - **expired_at**    : Timestampt when the session expired (Datetime)

    """

    __tablename__: str = "sessions"

    id_: UUID = Field(primary_key=True)
    refresh_token_hash: str
    user_agent: str | None
    user_id: UUID = Field(foreign_key="users.id_")
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True)),
    )
    expired_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True)),
    )
    revoked_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True)),
    )
    rotated_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True)),
    )
