from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.payment_provider import PaymentProvider


class PaymentProviderRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_active_by_business_and_provider(
        self,
        *,
        business_id: str,
        provider: str,
    ) -> PaymentProvider | None:
        stmt = select(PaymentProvider).where(
            PaymentProvider.business_id == business_id,
            PaymentProvider.provider == provider,
            PaymentProvider.is_active.is_(True),
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(
        self,
        *,
        business_id: str,
        provider: str,
        public_key_encrypted: str | None,
        secret_key_encrypted: str,
        webhook_secret_encrypted: str | None,
    ) -> PaymentProvider:
        payment_provider = PaymentProvider(
            business_id=business_id,
            provider=provider,
            public_key_encrypted=public_key_encrypted,
            secret_key_encrypted=secret_key_encrypted,
            webhook_secret_encrypted=webhook_secret_encrypted,
            is_active=True,
        )
        self.db.add(payment_provider)
        await self.db.flush()
        return payment_provider