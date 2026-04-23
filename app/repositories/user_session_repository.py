from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_session import UserSession


class UserSessionRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_id(self, session_id: str) -> UserSession | None:
        result = await self.db.execute(select(UserSession).where(UserSession.id == session_id))
        return result.scalar_one_or_none()

    async def create(
        self,
        *,
        user_id: str,
        business_id: str,
        refresh_token_hash: str,
        expires_at: datetime,
        user_agent: str | None = None,
        ip_address: str | None = None,
    ) -> UserSession:
        session = UserSession(
            user_id=user_id,
            business_id=business_id,
            refresh_token_hash=refresh_token_hash,
            expires_at=expires_at,
            user_agent=user_agent,
            ip_address=ip_address,
        )
        self.db.add(session)
        await self.db.flush()
        return session

    async def revoke(self, session: UserSession) -> None:
        session.is_revoked = True
        session.revoked_at = datetime.now(UTC)
        await self.db.flush()

    async def touch(self, session: UserSession) -> None:
        session.last_used_at = datetime.now(UTC)
        await self.db.flush()