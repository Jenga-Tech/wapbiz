from __future__ import annotations

from datetime import UTC, datetime, timedelta
from secrets import token_urlsafe
from typing import Any

import jwt
from pwdlib import PasswordHash

from app.core.config import get_settings

settings = get_settings()
password_hasher = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return password_hasher.verify(password, password_hash)


def generate_session_token() -> str:
    return token_urlsafe(48)


def _build_token(
    *,
    subject: str,
    token_type: str,
    secret: str,
    expires_delta: timedelta,
    extra_claims: dict[str, Any] | None = None,
) -> str:
    now = datetime.now(UTC)
    payload: dict[str, Any] = {
        "sub": subject,
        "type": token_type,
        "iss": settings.jwt_issuer,
        "aud": settings.jwt_audience,
        "iat": int(now.timestamp()),
        "nbf": int(now.timestamp()),
        "exp": int((now + expires_delta).timestamp()),
    }

    if extra_claims:
        payload.update(extra_claims)

    return jwt.encode(payload, secret, algorithm="HS256")


def create_access_token(
    *,
    subject: str,
    business_id: str,
    role: str,
) -> str:
    return _build_token(
        subject=subject,
        token_type="access",
        secret=settings.jwt_access_token_secret,
        expires_delta=timedelta(minutes=settings.jwt_access_token_expires_minutes),
        extra_claims={
            "business_id": business_id,
            "role": role,
        },
    )


def create_refresh_token(
    *,
    subject: str,
    session_id: str,
) -> str:
    return _build_token(
        subject=subject,
        token_type="refresh",
        secret=settings.jwt_refresh_token_secret,
        expires_delta=timedelta(days=settings.jwt_refresh_token_expires_days),
        extra_claims={
            "session_id": session_id,
        },
    )


def decode_access_token(token: str) -> dict[str, Any]:
    return jwt.decode(
        token,
        settings.jwt_access_token_secret,
        algorithms=["HS256"],
        audience=settings.jwt_audience,
        issuer=settings.jwt_issuer,
    )


def decode_refresh_token(token: str) -> dict[str, Any]:
    return jwt.decode(
        token,
        settings.jwt_refresh_token_secret,
        algorithms=["HS256"],
        audience=settings.jwt_audience,
        issuer=settings.jwt_issuer,
    )


def get_refresh_token_expiry() -> datetime:
    return datetime.now(UTC) + timedelta(days=settings.jwt_refresh_token_expires_days)