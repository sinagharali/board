from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import Column, DateTime, String
from sqlmodel import Field, Relationship

from common.models.base_orm_model import BaseORM

if TYPE_CHECKING:
    from user.model import User


class Board(BaseORM, table=True):
    """
    Board Model.

    Fields:
    - **id_** : Primary key (UUID)
    - **name** : Name (str)
    - **caption** : caption (str)
    - **avatar** : profile picture name (str)
    - **created_by** : Who created the board (UUID)
    - **creator** : The creator (User)
    - **created_at** : When Board Model is Created (DateTime)
    - **updated_at** : When User Model is Updated (DateTime)

    caption and avatar are **nullable**.
    """

    __tablename__: str = "boards"

    id_: UUID = Field(primary_key=True)
    name: str = Field(sa_column=Column(String(50)))
    avatar: str | None
    caption: str | None = Field(sa_column=Column(String(255)))
    created_by: UUID = Field(
        foreign_key="users.id_",
        ondelete="RESTRICT",
        nullable=False,
    )
    creator: Optional["User"] = Relationship()
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True)),
    )
    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True)),
    )
