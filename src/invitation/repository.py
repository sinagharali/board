from uuid import UUID

from sqlalchemy import Select

from database.base_repo import BaseRepository
from invitation.model import Invitation


class InvitationRepository(BaseRepository[Invitation]):
    async def get_by_target_and_invited_by(self, board_id: UUID, user_id: UUID):
        stmt = Select(Invitation).where(
            (Invitation.invited_by == user_id) & (Invitation.target_id == board_id),
        )
        result = await self.db_session.exec(stmt)
        return result.scalar_one_or_none()
