from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.models.business import Business
from app.models.user import User
from app.models.whatsapp_account import WhatsAppAccount
from app.repositories.business_user_repository import BusinessUserRepository
from app.repositories.setup_repository import SetupRepository
from app.schemas.business import CreateBusinessRequest
from app.utils.encryption import encrypt_value


class SetupService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.repo = SetupRepository(db)
        self.business_user_repo = BusinessUserRepository(db)

    async def create_business_with_owner_and_whatsapp(
        self,
        payload: CreateBusinessRequest,
    ) -> tuple[Business, User, WhatsAppAccount]:
        normalized_slug = payload.business_slug.strip().lower()
        normalized_owner_email = payload.owner_email.strip().lower()

        existing_business = await self.db.scalar(
            select(Business).where(Business.slug == normalized_slug)
        )
        if existing_business is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Business slug already exists.",
            )

        existing_user = await self.db.scalar(
            select(User).where(User.email == normalized_owner_email)
        )
        if existing_user is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Owner email already exists.",
            )

        existing_whatsapp = await self.db.scalar(
            select(WhatsAppAccount).where(
                WhatsAppAccount.phone_number_id == payload.whatsapp_phone_number_id
            )
        )
        if existing_whatsapp is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="WhatsApp phone number ID already exists.",
            )

        business = await self.repo.create_business(
            name=payload.business_name.strip(),
            slug=normalized_slug,
            contact_email=payload.contact_email,
            contact_phone=payload.contact_phone,
            country=payload.country,
            currency=payload.currency.upper(),
            timezone=payload.timezone,
        )

        owner = await self.repo.create_owner_user(
            business_id=business.id,
            full_name=payload.owner_full_name.strip(),
            email=normalized_owner_email,
            password_hash=hash_password(payload.owner_password),
        )

        await self.business_user_repo.create(
            business_id=business.id,
            user_id=owner.id,
            role="owner",
        )

        whatsapp_account = await self.repo.create_whatsapp_account(
            business_id=business.id,
            phone_number_id=payload.whatsapp_phone_number_id,
            waba_id=payload.whatsapp_waba_id,
            business_phone=payload.whatsapp_business_phone,
            verify_token=payload.whatsapp_verify_token,
            access_token_encrypted=encrypt_value(payload.whatsapp_access_token),
            app_secret_encrypted=encrypt_value(payload.whatsapp_app_secret)
            if payload.whatsapp_app_secret
            else None,
        )

        await self.db.commit()
        return business, owner, whatsapp_account