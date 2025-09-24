from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv

from auth.provider import get_current_user
from invitation.dependencies import get_invitation_service
from invitation.schemas import CreateInvitationDto
from invitation.service import InvitationService
from user.model import User

router = APIRouter(tags=["Invitation"])


@cbv(router)
class InvitationCBV:
    def __init__(
        self,
        invitation_service: Annotated[
            InvitationService,
            Depends(get_invitation_service),
        ],
    ):
        self.invitation_service = invitation_service

    @router.post("/boards/{board_id}/invites")
    async def create_invitation(
        self,
        board_id: UUID,
        user: Annotated[User, Depends(get_current_user)],
        dto: CreateInvitationDto,
    ):
        return await self.invitation_service.create_invitation(dto, user, board_id)

    @router.delete("/boards/{board_id}/invites/{invitation_id}")
    async def delete_invitation(
        self,
        board_id: UUID,
        invitation_id: UUID,
        user: Annotated[User, Depends(get_current_user)],
    ):
        return await self.invitation_service.delete_invitation(
            invitation_id,
            board_id,
            user,
        )

    @router.patch("/boards/{board_id}/invites/{invitation_id}/accept")
    async def accept_invitation(
        self,
        board_id: UUID,
        invitation_id: UUID,
        user: Annotated[User, Depends(get_current_user)],
    ):
        return await self.invitation_service.accept_invitation(
            user,
            board_id,
            invitation_id,
        )

    @router.delete("/boards/{board_id}/invites/{invitation_id}/reject")
    async def reject_invitation(
        self,
        board_id: UUID,
        invitation_id: UUID,
        user: Annotated[User, Depends(get_current_user)],
    ):
        return await self.invitation_service.reject_invitation(
            user,
            board_id,
            invitation_id,
        )

    @router.get("/boards/{board_id}/invites/{invite_id}/")
    async def get_specific_invitation(
        self,
        board_id: UUID,
        invite_id: UUID,
        user: Annotated[User, Depends(get_current_user)],
    ): ...

    @router.get("/boards/{board_id}/invites/")
    async def get_invitations(
        self,
        board_id: UUID,
        user: Annotated[User, Depends(get_current_user)],
    ): ...

    @router.get("/invites/received/")
    async def get_received_invitations(
        self,
        user: Annotated[User, Depends(get_current_user)],
        limit: int = 50,
        offset: int = 0,
    ): ...
