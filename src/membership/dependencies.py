from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import get_session
from membership.repository import MembershipRepository
from membership.service import MembershipService


def get_membership_service(
    db_session: Annotated[AsyncSession, Depends(get_session)],
) -> MembershipService:
    membership_repo = MembershipRepository(db_session)
    return MembershipService(membership_repo=membership_repo)
