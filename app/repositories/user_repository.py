from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_id(self, user_id: str) -> User | None:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create(
        self,
        *,
        business_id: str,
        email: str,
        full_name: str,
        password_hash: str,
        role: str,
    ) -> User:
        user = User(
            business_id=business_id,
            email=email,
            full_name=full_name,
            password_hash=password_hash,
            role=role,
        )
        self.db.add(user)
        await self.db.flush()
        return user