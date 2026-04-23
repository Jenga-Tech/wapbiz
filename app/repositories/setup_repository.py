from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.business import Business
from app.models.user import User
from app.models.whatsapp_account import WhatsAppAccount


class SetupRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_business(
        self,
        *,
        name: str,
        slug: str,
        contact_email: str | None,
        contact_phone: str | None,
        country: str | None,
        currency: str,
        timezone: str,
    ) -> Business:
        business = Business(
            name=name,
            slug=slug,
            contact_email=contact_email,
            contact_phone=contact_phone,
            country=country,
            currency=currency,
            timezone=timezone,
        )
        self.db.add(business)
        await self.db.flush()
        return business

    async def create_owner_user(
        self,
        *,
        business_id: str,
        full_name: str,
        email: str,
        password_hash: str,
    ) -> User:
        user = User(
            business_id=business_id,
            full_name=full_name,
            email=email,
            password_hash=password_hash,
            role="owner",
            is_active=True,
        )
        self.db.add(user)
        await self.db.flush()
        return user

    async def create_whatsapp_account(
        self,
        *,
        business_id: str,
        phone_number_id: str,
        waba_id: str,
        business_phone: str,
        verify_token: str,
        access_token_encrypted: str,
        app_secret_encrypted: str | None,
    ) -> WhatsAppAccount:
        whatsapp_account = WhatsAppAccount(
            business_id=business_id,
            phone_number_id=phone_number_id,
            waba_id=waba_id,
            business_phone=business_phone,
            verify_token=verify_token,
            access_token_encrypted=access_token_encrypted,
            app_secret_encrypted=app_secret_encrypted,
            webhook_status="pending",
            is_active=True,
        )
        self.db.add(whatsapp_account)
        await self.db.flush()
        return whatsapp_account