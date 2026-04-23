from __future__ import annotations

from datetime import UTC, datetime

from fastapi import HTTPException, status
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    get_refresh_token_expiry,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.repositories.user_session_repository import UserSessionRepository


class AuthService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.user_repo = UserRepository(db)
        self.session_repo = UserSessionRepository(db)

    async def authenticate_user(self, *, email: str, password: str) -> User:
        user = await self.user_repo.get_by_email(email)
        if user is None or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        if not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        return user

    async def login(
        self,
        *,
        email: str,
        password: str,
        user_agent: str | None = None,
        ip_address: str | None = None,
    ) -> dict[str, str]:
        user = await self.authenticate_user(email=email, password=password)

        placeholder_refresh_value = hash_password(f"{user.id}:{datetime.now(UTC).timestamp()}")
        session = await self.session_repo.create(
            user_id=user.id,
            business_id=user.business_id,
            refresh_token_hash=placeholder_refresh_value,
            expires_at=get_refresh_token_expiry(),
            user_agent=user_agent,
            ip_address=ip_address,
        )

        refresh_token = create_refresh_token(subject=user.id, session_id=session.id)
        session.refresh_token_hash = hash_password(refresh_token)
        await self.db.flush()

        access_token = create_access_token(
            subject=user.id,
            business_id=user.business_id,
            role=user.role,
        )

        await self.db.commit()

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    async def refresh_tokens(self, *, refresh_token: str) -> dict[str, str]:
        try:
            payload = decode_refresh_token(refresh_token)
        except InvalidTokenError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token.",
            ) from exc

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type.",
            )

        user_id = payload.get("sub")
        session_id = payload.get("session_id")
        if not user_id or not session_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Malformed refresh token.",
            )

        session = await self.session_repo.get_by_id(session_id)
        if session is None or session.is_revoked:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session is invalid or revoked.",
            )

        if session.expires_at <= datetime.now(UTC):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session has expired.",
            )

        if not verify_password(refresh_token, session.refresh_token_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token mismatch.",
            )

        user = await self.user_repo.get_by_id(user_id)
        if user is None or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User account is not active.",
            )

        new_refresh_token = create_refresh_token(subject=user.id, session_id=session.id)
        session.refresh_token_hash = hash_password(new_refresh_token)
        await self.session_repo.touch(session)

        new_access_token = create_access_token(
            subject=user.id,
            business_id=user.business_id,
            role=user.role,
        )

        await self.db.commit()

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
        }