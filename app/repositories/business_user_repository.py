from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.business_user import BusinessUser


class BusinessUserRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_business_and_user(
        self,
        *,
        business_id: str,
        user_id: str,
    ) -> BusinessUser | None:
        result = await self.db.execute(
            select(BusinessUser).where(
                BusinessUser.business_id == business_id,
                BusinessUser.user_id == user_id,
            )
        )
        return result.scalar_one_or_none()

    async def list_by_business(self, business_id: str) -> list[BusinessUser]:
        result = await self.db.execute(
            select(BusinessUser).where(BusinessUser.business_id == business_id)
        )
        return list(result.scalars().all())

    async def create(
        self,
        *,
        business_id: str,
        user_id: str,
        role: str,
    ) -> BusinessUser:
        membership = BusinessUser(
            business_id=business_id,
            user_id=user_id,
            role=role,
        )
        self.db.add(membership)
        await self.db.flush()
        return membership