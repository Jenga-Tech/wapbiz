from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.whatsapp_account import WhatsAppAccount


class WhatsAppAccountRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_phone_number_id(self, phone_number_id: str) -> WhatsAppAccount | None:
        stmt = select(WhatsAppAccount).where(WhatsAppAccount.phone_number_id == phone_number_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_verify_token(self, verify_token: str) -> WhatsAppAccount | None:
        stmt = select(WhatsAppAccount).where(WhatsAppAccount.verify_token == verify_token)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()