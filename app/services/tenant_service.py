from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.business_repository import BusinessRepository
from app.repositories.business_settings_repository import BusinessSettingsRepository
from app.repositories.business_user_repository import BusinessUserRepository
from app.schemas.business_settings import UpsertBusinessSettingsRequest
from app.schemas.business_user import CreateBusinessUserRequest


class TenantService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.business_repo = BusinessRepository(db)
        self.settings_repo = BusinessSettingsRepository(db)
        self.business_user_repo = BusinessUserRepository(db)

    async def upsert_business_settings(
        self,
        payload: UpsertBusinessSettingsRequest,
    ) -> dict:
        business = await self.business_repo.get_by_id(payload.business_id)
        if business is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Business not found.",
            )

        settings = await self.settings_repo.create_or_update(
            business_id=payload.business_id,
            brand_name=payload.brand_name,
            logo_url=payload.logo_url,
            support_email=payload.support_email,
            support_phone=payload.support_phone,
            receipt_footer=payload.receipt_footer,
        )
        await self.db.commit()

        return {
            "business_id": settings.business_id,
            "brand_name": settings.brand_name,
            "logo_url": settings.logo_url,
            "support_email": settings.support_email,
            "support_phone": settings.support_phone,
            "receipt_footer": settings.receipt_footer,
        }

    async def add_business_user(
        self,
        payload: CreateBusinessUserRequest,
    ) -> dict:
        business = await self.business_repo.get_by_id(payload.business_id)
        if business is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Business not found.",
            )

        existing = await self.business_user_repo.get_by_business_and_user(
            business_id=payload.business_id,
            user_id=payload.user_id,
        )
        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is already a member of this business.",
            )

        membership = await self.business_user_repo.create(
            business_id=payload.business_id,
            user_id=payload.user_id,
            role=payload.role,
        )
        await self.db.commit()

        return {
            "id": membership.id,
            "business_id": membership.business_id,
            "user_id": membership.user_id,
            "role": membership.role,
        }