from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth import TokenService, get_token_service
from database.engine import get_session
from session.repository import SessionRepository
from session.service import SessionService


def get_session_service(
    db_session: Annotated[AsyncSession, Depends(get_session)],
    token_service: Annotated[TokenService, Depends(get_token_service)],
) -> SessionService:
    session_repo = SessionRepository(db_session)
    return SessionService(session_repo=session_repo, token_service=token_service)
