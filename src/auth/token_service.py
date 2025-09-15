from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any
from uuid import UUID, uuid4

import jwt
from jwt import ExpiredSignatureError
from jwt import InvalidTokenError as PyJWTInvalidTokenError

from auth.errors import AuthError, AuthErrors


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class TokenService:
    def __init__(
        self,
        access_secret_key: str,
        refresh_secret_key: str,
        algorithm: str,
        access_expiry_minutes: int,
        refresh_expiry_days: int,
    ):
        self.access_secret_key = access_secret_key
        self.refresh_secret_key = refresh_secret_key
        self.algorithm = algorithm
        self.access_expiry_minutes = access_expiry_minutes
        self.refresh_expiry_days = refresh_expiry_days

    def _utcnow(self) -> datetime:
        return datetime.now(timezone.utc)

    def _make_serializable(self, data: dict[str, Any]) -> dict[str, Any]:
        def serialize(value):  # -> str | Any:
            if isinstance(value, UUID):
                return str(value)
            return value

        return {k: serialize(v) for k, v in data.items()}

    def create_access_token(self, claims: dict) -> str:
        expires = self._utcnow() + timedelta(minutes=self.access_expiry_minutes)
        claims["type"] = "access"
        full_payload = {
            **claims,
            "exp": int(expires.timestamp()),
            "iat": int(self._utcnow().timestamp()),
            "jti": str(uuid4()),
        }
        serializable_payload = self._make_serializable(full_payload)
        return jwt.encode(
            serializable_payload,
            key=self.access_secret_key,
            algorithm=self.algorithm,
        )

    def create_refresh_token(self, claims: dict) -> str:
        expires = self._utcnow() + timedelta(days=self.refresh_expiry_days)
        claims["type"] = "refresh"
        full_payload = {
            **claims,
            "exp": int(expires.timestamp()),
            "iat": int(self._utcnow().timestamp()),
            "jti": str(uuid4()),
        }
        serializable_payload = self._make_serializable(full_payload)
        return jwt.encode(
            serializable_payload,
            key=self.access_secret_key,
            algorithm=self.algorithm,
        )

    def decode_token(self, token: str, *, expected_type: TokenType) -> dict:
        if not token:
            raise AuthError(AuthErrors.TOKEN_MISSING)

        key, required_claims = {
            TokenType.ACCESS: (self.access_secret_key, {"sub", "email"}),
            TokenType.REFRESH: (
                self.refresh_secret_key,
                {"sub", "session_id", "email"},
            ),
        }.get(expected_type, (None, None))

        if key is None:
            raise AuthError(AuthErrors.MISMATCH_TOKEN_TYPE)

        try:
            payload = jwt.decode(token, key=key, algorithms=[self.algorithm])
            missing = required_claims - payload.keys()
            if missing:
                raise AuthError(AuthErrors.INVALID_TOKEN)
        except ExpiredSignatureError as exc:
            raise AuthError(AuthErrors.EXPIRED_SIGNATURE) from exc
        except PyJWTInvalidTokenError as exc:
            raise AuthError(AuthErrors.INVALID_TOKEN) from exc

        return payload
