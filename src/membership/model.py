from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import Column, DateTime, ForeignKey
from sqlmodel import Field, Relationship

from common.models.base_orm_model import BaseORM

if TYPE_CHECKING:
    from board.model import Board
    from user.model import User


class MembershipRole(str, Enum):
    ADMIN = "admin"
    MEMBER = "member"


class Membership(BaseORM, table=True):
    """
    Mmebership Model.

    Fields:
    - **member_id** : Primary key (UUID) and Foriegn key (UUID)
    - **member** : User
    - **board_id** : Primary key (UUID) and Foriegn key (UUID)
    - **board** : Board
    - **role** : Role (MembershipRole) either member or admin
    - **created_at** : When Membership Model is Created (DateTime)
    - **updated_at** : When Membership Model is Updated (DateTime)

    """

    __tablename__: str = "memberships"
    member_id: UUID = Field(
        default=None,
        sa_column=Column(ForeignKey("users.id_"), primary_key=True),
    )
    member: Optional["User"] = Relationship()
    board_id: UUID = Field(
        default=None,
        sa_column=Column(ForeignKey("boards.id_"), primary_key=True),
    )
    board: Optional["Board"] = Relationship()
    role: MembershipRole
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True)))
    updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True)))
