from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv

from auth.provider import get_current_user
from user.model import User

router = APIRouter(tags=["Mmebership"])


@cbv(router)
class MembershipCBV:
    @router.get("/memberships/")
    async def get_memberships(
        self,
        board_id: UUID,
        user: Annotated[User, Depends(get_current_user)],
        limit: int = 50,
        offset: int = 0,
        role: str | None = None,  # optional filter by role
    ): ...

    @router.get("/memberships/{member_id}/")
    async def get_membership(
        self,
        board_id: UUID,
        member_id: UUID,
        user: Annotated[User, Depends(get_current_user)],
    ): ...

    @router.get("/boards/{board_id}/memberships/{member_id}/")
    async def get_board_membership(
        self,
        board_id: UUID,
        member_id: UUID,
        user: Annotated[User, Depends(get_current_user)],
    ): ...

    @router.patch("/boards/{board_id}/memberships/{member_id}/upgrade-to-admin/")
    async def upgrade_to_admin(
        self,
        board_id: UUID,
        member_id: UUID,
        user: Annotated[User, Depends(get_current_user)],
        roles: list[str] | None = None,  # optional roles to assign on upgrade
    ): ...

    @router.patch("/boards/{board_id}/memberships/{member_id}/add-roles/")
    async def add_roles_to_admin(
        self,
        board_id: UUID,
        member_id: UUID,
        user: Annotated[User, Depends(get_current_user)],
        roles: list[str],
    ): ...

    @router.patch("/boards/{board_id}/memberships/{member_id}/downgrade-to-member/")
    async def downgrade_to_member(
        self,
        board_id: UUID,
        member_id: UUID,
        user: Annotated[User, Depends(get_current_user)],
    ): ...

    @router.delete("/boards/{board_id}/memberships/{member_id}/")
    async def revoke_membership(
        self,
        board_id: UUID,
        member_id: UUID,
        user: Annotated[User, Depends(get_current_user)],
    ): ...
