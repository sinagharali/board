from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from acl.dependencies import get_authorization_service
from acl.openfga_authorization import AuthorizationService
from database.engine import get_session
from invitation.repository import InvitationRepository
from invitation.service import InvitationService
from membership.dependencies import get_membership_service
from membership.service import MembershipService
from user.dependencies import get_user_service
from user.service import UserService


async def get_invitation_service(
    db_session: Annotated[AsyncSession, Depends(get_session)],
    authorization_service: Annotated[
        AuthorizationService,
        Depends(get_authorization_service),
    ],
    user_service: Annotated[UserService, Depends(get_user_service)],
    membership_service: Annotated[MembershipService, Depends(get_membership_service)],
):
    invitation_repo = InvitationRepository(db_session)
    return InvitationService(
        invitation_repo=invitation_repo,
        user_service=user_service,
        authorization_service=authorization_service,
        membership_service=membership_service,
    )
