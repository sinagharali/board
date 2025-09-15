from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import get_session
from user.repository import UserRepository
from user.service import UserService


def get_user_service(
    db_session: Annotated[AsyncSession, Depends(get_session)],
) -> UserService:
    user_repo = UserRepository(db_session)
    return UserService(user_repo=user_repo)
