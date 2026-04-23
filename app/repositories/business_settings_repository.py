from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.business_settings import BusinessSettings


class BusinessSettingsRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_business_id(self, business_id: str) -> BusinessSettings | None:
        result = await self.db.execute(
            select(BusinessSettings).where(BusinessSettings.business_id == business_id)
        )
        return result.scalar_one_or_none()

    async def create_or_update(
        self,
        *,
        business_id: str,
        brand_name: str | None = None,
        logo_url: str | None = None,
        support_email: str | None = None,
        support_phone: str | None = None,
        receipt_footer: str | None = None,
    ) -> BusinessSettings:
        settings = await self.get_by_business_id(business_id)

        if settings is None:
            settings = BusinessSettings(
                business_id=business_id,
                brand_name=brand_name,
                logo_url=logo_url,
                support_email=support_email,
                support_phone=support_phone,
                receipt_footer=receipt_footer,
            )
            self.db.add(settings)
            await self.db.flush()
            return settings

        settings.brand_name = brand_name
        settings.logo_url = logo_url
        settings.support_email = support_email
        settings.support_phone = support_phone
        settings.receipt_footer = receipt_footer
        await self.db.flush()
        return settings