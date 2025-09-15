from fastapi.security import HTTPAuthorizationCredentials

from auth.errors import AuthError, AuthErrors
from auth.token_service import TokenService, TokenType
from user.model import User
from user.service import UserService


class UserAuthenticator:
    def __init__(self, token_service: TokenService, user_service: UserService):
        self.token_service = token_service
        self.user_service = user_service

    def _decode_token(self, token):
        payload = self.token_service.decode_token(
            token=token,
            expected_type=TokenType.ACCESS,
        )
        return payload

    async def get_current_user(self, credentials: HTTPAuthorizationCredentials) -> User:
        token = credentials.credentials
        payload = self._decode_token(token)

        user_id = payload.get("sub")
        if not user_id:  # For safety.
            raise AuthError(AuthErrors.INVALID_TOKEN)

        return await self.user_service.ensure_user_exists_by_id(user_id)
