from fastapi import Request

from auth.errors import AuthError, AuthErrors
from auth.schemas import SigninDto, SignupDto
from auth.token_service import TokenService, TokenType
from common.utils.hash import verify_plain
from session.service import SessionService
from user.service import UserService


class AuthService:
    def __init__(
        self,
        user_service: UserService,
        token_service: TokenService,
        session_service: SessionService,
    ):
        self.user_service = user_service
        self.token_service = token_service
        self.session_service = session_service

    async def signup(self, req: Request, dto: SignupDto):
        lower_email = dto.email.lower()

        # Ensure User does not exist.
        await self.user_service.ensure_user_not_exists_by_email(lower_email)

        # Get user agent from request.
        user_agent = req.headers.get("user-agent") or None

        # Create user.
        new_user = await self.user_service.create_user(dto)

        # Create tokens.
        access_token = self.token_service.create_access_token(
            {"sub": new_user.id_, "email": lower_email},
        )
        refresh_token = await self.session_service.persist_session(
            user_agent,
            lower_email,
            new_user.id_,
        )

        # Return tokens and user without sensitive data like password.
        return {
            "access": access_token,
            "refresh": refresh_token,
            "user": new_user.serializable_dict(exclude_list=["password"]),
        }

    async def signin(self, req: Request, dto: SigninDto):
        lower_email = dto.email.lower()

        # Ensure user exists.
        user = await self.user_service.ensure_user_exists_by_email(
            lower_email,
        )

        # Compare password.
        if not verify_plain(dto.password, user.password):
            raise AuthError(AuthErrors.WRONG_PASSWORD)

        # Get user agent from request.
        user_agent = req.headers.get("user-agent") or None

        # Create Tokens.
        access_token = self.token_service.create_access_token(
            {"sub": user.id_, "email": lower_email},
        )
        refresh_token = await self.session_service.persist_session(
            user_agent,
            lower_email,
            user.id_,
        )

        # Return tokens and user without sensitive data like password.
        return {
            "access": access_token,
            "refresh": refresh_token,
            "user": user.serializable_dict(exclude_list=["password"]),
        }

    async def refresh(self, refresh_token: str):
        # Decode token.
        payload = self.token_service.decode_token(
            refresh_token,
            expected_type=TokenType.REFRESH,
        )

        user = await self.user_service.ensure_user_exists_by_id(
            payload["sub"],
        )

        # Validate session.
        session = await self.session_service.validate_session(
            payload["session_id"],
            refresh_token,
        )
        # Update session and create new refresh token.
        new_refresh_token = await self.session_service.rotate_session(
            session,
            payload["email"],
        )

        # Create tokens.
        access_token = self.token_service.create_access_token(
            {"sub": user.id_, "email": user.email},
        )

        # Return tokens and user without sensitive data like password.
        return {
            "access": access_token,
            "refresh": new_refresh_token,
            "user": user.serializable_dict(exclude_list=["password"]),
        }

    async def signout(self, refresh_token: str):
        # Decode token.
        payload = self.token_service.decode_token(
            refresh_token,
            expected_type=TokenType.REFRESH,
        )

        await self.session_service.revoke_session(payload["session_id"])
