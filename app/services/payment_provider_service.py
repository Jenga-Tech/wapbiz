from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.business_repository import BusinessRepository
from app.repositories.payment_provider_repository import PaymentProviderRepository
from app.schemas.payment_provider import CreatePaymentProviderRequest
from app.utils.encryption import encrypt_value


class PaymentProviderService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.business_repo = BusinessRepository(db)
        self.provider_repo = PaymentProviderRepository(db)

    async def create_payment_provider(
        self,
        payload: CreatePaymentProviderRequest,
    ) -> dict:
        business = await self.business_repo.get_by_id(payload.business_id)
        if business is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Business not found.",
            )

        existing = await self.provider_repo.get_active_by_business_and_provider(
            business_id=payload.business_id,
            provider=payload.provider,
        )
        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Active payment provider already exists for this business.",
            )

        provider = await self.provider_repo.create(
            business_id=payload.business_id,
            provider=payload.provider,
            public_key_encrypted=encrypt_value(payload.public_key) if payload.public_key else None,
            secret_key_encrypted=encrypt_value(payload.secret_key),
            webhook_secret_encrypted=encrypt_value(payload.webhook_secret)
            if payload.webhook_secret
            else None,
        )
        await self.db.commit()

        return {
            "payment_provider_id": provider.id,
            "business_id": provider.business_id,
            "provider": provider.provider,
            "message": "Payment provider created successfully.",
        }