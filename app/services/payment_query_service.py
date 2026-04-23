from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.payment_repository import PaymentRepository


class PaymentQueryService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.payment_repo = PaymentRepository(db)

    async def list_payments(self, business_id: str) -> list[dict]:
        payments = await self.payment_repo.list_by_business(business_id)
        return [
            {
                "id": payment.id,
                "business_id": payment.business_id,
                "order_id": payment.order_id,
                "provider": payment.provider,
                "provider_reference": payment.provider_reference,
                "status": payment.status,
                "amount": str(payment.amount),
                "currency": payment.currency,
                "authorization_url": payment.authorization_url,
                "access_code": payment.access_code,
                "paid_at": payment.paid_at.isoformat() if payment.paid_at else None,
            }
            for payment in payments
        ]

    async def list_payments_for_order(self, order_id: str) -> list[dict]:
        payments = await self.payment_repo.get_by_order_id(order_id)
        return [
            {
                "id": payment.id,
                "business_id": payment.business_id,
                "order_id": payment.order_id,
                "provider": payment.provider,
                "provider_reference": payment.provider_reference,
                "status": payment.status,
                "amount": str(payment.amount),
                "currency": payment.currency,
                "authorization_url": payment.authorization_url,
                "access_code": payment.access_code,
                "paid_at": payment.paid_at.isoformat() if payment.paid_at else None,
            }
            for payment in payments
        ]