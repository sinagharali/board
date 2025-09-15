from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from auth.config import auth_settings as settings
from auth.security import UserAuthenticator
from auth.token_service import TokenService
from user.dependencies import get_user_service
from user.model import User
from user.service import UserService

bearer_scheme = HTTPBearer()


def get_token_service() -> TokenService:
    return TokenService(
        access_secret_key=settings.access_token_secret_key,
        refresh_secret_key=settings.refresh_token_secret_key,
        algorithm=settings.alg,
        access_expiry_minutes=settings.access_token_expire_minutes,
        refresh_expiry_days=settings.refresh_token_expire_days,
    )


def get_user_authenticator(
    user_service: Annotated[UserService, Depends(get_user_service)],
    token_service: Annotated[TokenService, Depends(get_token_service)],
) -> UserAuthenticator:
    return UserAuthenticator(
        user_service=user_service,
        token_service=token_service,
    )


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
    auth: Annotated[UserAuthenticator, Depends(get_user_authenticator)],
) -> User:
    return await auth.get_current_user(credentials)
