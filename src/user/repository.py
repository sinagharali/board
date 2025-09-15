from sqlalchemy import select

from database.base_repo import BaseRepository
from user.model import User


class UserRepository(BaseRepository[User]):
    async def get_by_email(self, email: str) -> User | None:
        """
        Get user by email.

        Args:
            email: (str)

        Returns:
            UserModel | None.

        """
        stmt = select(User).where(User.email == email)
        result = await self.db_session.exec(stmt)
        return result.scalar_one_or_none()
