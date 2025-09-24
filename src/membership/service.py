from datetime import datetime, timezone
from uuid import UUID
from membership.errors import MembershipError, MembershipErrors
from membership.model import Membership, MembershipRole
from membership.repository import MembershipRepository


class MembershipService:
    def __init__(self, membership_repo: MembershipRepository):
        self.membership_repo = membership_repo

    async def ensure_user_is_not_member(self, user_id, board_id):
        membership = await self.membership_repo.get_by_board_and_user(board_id, user_id)

        if membership:
            raise MembershipError(MembershipErrors.ALREADY_MEMBER)

    async def create_membership(self, board_id: UUID, user_id: UUID) -> Membership:
        now = datetime.now(timezone.utc)
        return await self.membership_repo.create(
            Membership(
                member_id=user_id,
                board_id=board_id,
                role=MembershipRole.MEMBER,
                created_at=now,
                updated_at=now,
            ),
        )
