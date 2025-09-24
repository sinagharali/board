from uuid import UUID

from sqlalchemy import Select

from database.base_repo import BaseRepository
from membership.model import Membership


class MembershipRepository(BaseRepository[Membership]):
    async def get_by_board_and_user(self, board_id: UUID, user_id: UUID):
        stmt = Select(Membership).where(
            (Membership.board_id == board_id) & (Membership.member_id == user_id),
        )
        result = await self.db_session.exec(stmt)
        return result.scalar_one_or_none()
