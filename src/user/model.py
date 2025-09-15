from datetime import datetime
from uuid import UUID

from sqlmodel import Column, DateTime, Field, String

from common.models.base_orm_model import BaseORM


class User(BaseORM, table=True):
    """
    User Model.

    Fields:
    - **id_** : Primary key (UUID)
    - **name** : Name (str)
    - **email** : Email (str)
    - **password** : Hashed Password (str)
    - **created_at** : When User Model is Created (DateTime)
    - **updated_at** : When User Model is Updated (DateTime)
    """

    __tablename__: str = "users"

    id_: UUID = Field(primary_key=True)
    name: str = Field(max_length=100)
    email: str = Field(sa_column=Column(String(255), unique=True, index=True))
    password: str = Field(max_length=64)
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True)),
    )
    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True)),
    )
