from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.payment import Payment


class PaymentRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_reference(self, provider_reference: str) -> Payment | None:
        stmt = select(Payment).where(Payment.provider_reference == provider_reference)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_order_id(self, order_id: str) -> list[Payment]:
        stmt = select(Payment).where(Payment.order_id == order_id).order_by(Payment.created_at.desc())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def list_by_business(self, business_id: str) -> list[Payment]:
        stmt = select(Payment).where(Payment.business_id == business_id).order_by(Payment.created_at.desc())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(
        self,
        *,
        business_id: str,
        order_id: str,
        provider: str,
        provider_reference: str,
        amount: Decimal,
        currency: str,
        authorization_url: str | None = None,
        access_code: str | None = None,
        raw_payload: dict | None = None,
    ) -> Payment:
        payment = Payment(
            business_id=business_id,
            order_id=order_id,
            provider=provider,
            provider_reference=provider_reference,
            amount=amount,
            currency=currency,
            authorization_url=authorization_url,
            access_code=access_code,
            raw_payload=raw_payload,
            status="initialized",
        )
        self.db.add(payment)
        await self.db.flush()
        return payment

    async def mark_paid(self, payment: Payment, raw_payload: dict | None = None) -> Payment:
        payment.status = "paid"
        payment.paid_at = datetime.now(UTC)
        if raw_payload is not None:
            payment.raw_payload = raw_payload
        await self.db.flush()
        return payment

    async def mark_failed(self, payment: Payment, raw_payload: dict | None = None) -> Payment:
        payment.status = "failed"
        if raw_payload is not None:
            payment.raw_payload = raw_payload
        await self.db.flush()
        return payment