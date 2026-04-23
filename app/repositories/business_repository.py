from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.business import Business
from app.models.whatsapp_account import WhatsAppAccount


class BusinessRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_id(self, business_id: str) -> Business | None:
        result = await self.db.execute(select(Business).where(Business.id == business_id))
        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Business | None:
        result = await self.db.execute(select(Business).where(Business.slug == slug))
        return result.scalar_one_or_none()

    async def get_by_phone_number_id(self, phone_number_id: str) -> Business | None:
        stmt = (
            select(Business)
            .join(WhatsAppAccount, WhatsAppAccount.business_id == Business.id)
            .where(WhatsAppAccount.phone_number_id == phone_number_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_business_and_whatsapp_account(
        self,
        phone_number_id: str,
    ) -> tuple[Business | None, WhatsAppAccount | None]:
        stmt = (
            select(Business, WhatsAppAccount)
            .join(WhatsAppAccount, WhatsAppAccount.business_id == Business.id)
            .where(WhatsAppAccount.phone_number_id == phone_number_id)
        )
        result = await self.db.execute(stmt)
        row = result.first()

        if row is None:
            return None, None

        return row[0], row[1]