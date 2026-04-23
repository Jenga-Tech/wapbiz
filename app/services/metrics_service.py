from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.customer import Customer
from app.models.order import Order
from app.models.payment import Payment
from app.models.receipt import Receipt


class MetricsService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_basic_metrics(self, business_id: str) -> dict:
        customer_count = await self.db.scalar(
            select(func.count()).select_from(Customer).where(Customer.business_id == business_id)
        )
        order_count = await self.db.scalar(
            select(func.count()).select_from(Order).where(Order.business_id == business_id)
        )
        paid_payment_count = await self.db.scalar(
            select(func.count())
            .select_from(Payment)
            .where(Payment.business_id == business_id, Payment.status == "paid")
        )
        receipt_count = await self.db.scalar(
            select(func.count()).select_from(Receipt).where(Receipt.business_id == business_id)
        )

        return {
            "business_id": business_id,
            "customers": customer_count or 0,
            "orders": order_count or 0,
            "paid_payments": paid_payment_count or 0,
            "receipts": receipt_count or 0,
        }