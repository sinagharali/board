from typing import Annotated

from fastapi import Depends

from auth.provider import get_token_service
from auth.service import AuthService
from auth.token_service import TokenService
from session import SessionService, get_session_service
from user import UserService, get_user_service


def get_auth_service(
    session_service: Annotated[SessionService, Depends(get_session_service)],
    token_service: Annotated[TokenService, Depends(get_token_service)],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> AuthService:
    return AuthService(
        session_service=session_service,
        token_service=token_service,
        user_service=user_service,
    )
