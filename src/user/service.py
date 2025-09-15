from datetime import datetime, timezone
from uuid import UUID, uuid4

from auth.schemas import SignupDto
from common.utils.hash import hash_password
from user.errors import UserError, UserErrors
from user.model import User
from user.repository import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def create_user(self, dto: SignupDto) -> User:
        now = datetime.now(timezone.utc)
        user = await self.user_repo.create(
            User(
                id_=uuid4(),
                name=dto.name,
                email=dto.email.lower(),
                password=hash_password(dto.password),
                created_at=now,
                updated_at=now,
            ),
        )
        return user

    async def ensure_user_exists_by_email(self, email: str):
        user = await self.user_repo.get_by_email(email)
        if not user:
            raise UserError(UserErrors.NOT_REGISTERED)
        return user

    async def ensure_user_not_exists_by_email(self, email: str):
        user = await self.user_repo.get_by_email(email)
        if user:
            raise UserError(UserErrors.ALREADY_REGISTERED)
        return user

    async def ensure_user_exists_by_id(self, user_id: UUID):
        user = await self.user_repo.get(User, user_id)
        if not user:
            raise UserError(UserErrors.NOT_REGISTERED)
        return user

    async def ensure_user_not_exists_by_id(self, user_id: UUID):
        user = await self.user_repo.get(User, user_id)
        if user:
            raise UserError(UserErrors.ALREADY_REGISTERED)
        return user
