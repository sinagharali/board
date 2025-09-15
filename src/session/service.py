from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4

from auth.token_service import TokenService
from common.utils.hash import hash_password, verify_plain
from session.config import session_settings as settings
from session.errors import SessionError, SessionErrors
from session.model import Session
from session.repository import SessionRepository


class SessionService:
    def __init__(self, session_repo: SessionRepository, token_service: TokenService):
        self.session_repo = session_repo
        self.token_service = token_service

    def _utc_now(self):
        return datetime.now(timezone.utc)

    async def persist_session(
        self,
        user_agent: str,
        email: str,
        user_id: UUID,
    ):
        session_id = uuid4()

        refresh_token = self.token_service.create_refresh_token(
            {
                "sub": user_id,
                "session_id": session_id,
                "email": email,
            },
        )
        await self.session_repo.create(
            Session(
                id_=session_id,
                user_id=user_id,
                user_agent=user_agent,
                refresh_token_hash=hash_password(refresh_token),
                created_at=self._utc_now(),
                expired_at=self._utc_now() + timedelta(days=settings.expire_days),
            ),
        )
        return refresh_token

    async def rotate_session(self, session: Session, email: str):
        now: datetime = self._utc_now()
        refresh_token = self.token_service.create_refresh_token(
            {
                "sub": session.user_id,
                "session_id": session.id_,
                "email": email,
            },
        )
        session.refresh_token_hash = hash_password(refresh_token)
        session.expired_at = now + timedelta(
            settings.expire_days,
        )
        session.rotated_at = now
        await self.session_repo.update(session)
        return refresh_token

    async def revoke_session(self, session_id: UUID):
        session = await self.session_repo.get(model=Session, id_=session_id)

        if not session:
            raise SessionError(SessionErrors.SESSION_NOT_FOUND)

        session.revoked_at = self._utc_now()
        await self.session_repo.update(session)

    async def validate_session(
        self,
        session_id: UUID,
        refresh_token: str,
    ) -> Session:
        session = await self.session_repo.get(
            model=Session,
            id_=session_id,
        )

        if session is None:
            raise SessionError(SessionErrors.SESSION_NOT_FOUND)

        now = datetime.now(timezone.utc)
        if session.expired_at < now:
            raise SessionError(SessionErrors.EXPIRED_SESSION)

        if session.revoked_at:
            raise SessionError(SessionErrors.REVOKED_SESSION)

        if not verify_plain(plain=refresh_token, hashed=session.refresh_token_hash):
            raise SessionError(SessionErrors.MISS_MATCH_REFRESH_TOKEN)

        return session
