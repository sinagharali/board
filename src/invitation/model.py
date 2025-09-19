from datetime import datetime
from uuid import UUID

from sqlalchemy import Column, DateTime, Enum, ForeignKey
from sqlmodel import Field

from common.models.base_orm_model import BaseORM
from membership.model import MembershipRole


class InvitationStatus(str, Enum):  # noqa: SLOT000
    PENDING = "pending"
    ACCEPTED = "accepted"


class Invitation(BaseORM, table=True):
    """
    Invitation Model.

    Fields:
    - **id_** = Primary Key (UUID)
    - **invited_by** : Foriegn key to User (UUID)
    - **invitee_email** : email belongs to the invited person (str)
    - **membership_role** : The role of the user (MembershipRole)
    - **status** : Status of the invitation: pending or accepted (InvitationStatus)
    - **target_id** : Foriegn key to board (UUID)
    - **created_at** : When Membership Model is Created (DateTime)

    """

    __tablename__: str = "invitations"
    id_: UUID = Field(primary_key=True)
    invited_by: UUID = Field(sa_column=Column(ForeignKey("users.id_")))
    invitee_email: str
    membership_role: MembershipRole
    status: InvitationStatus
    target_id: UUID = Field(sa_column=Column(ForeignKey("boards.id_")))
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True)))
