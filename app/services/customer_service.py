from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.customer import Customer


class CustomerService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def list_customers(self, business_id: str) -> list[dict]:
        result = await self.db.execute(
            select(Customer)
            .where(Customer.business_id == business_id)
            .order_by(Customer.last_seen_at.desc())
        )
        customers = list(result.scalars().all())

        return [
            {
                "id": customer.id,
                "business_id": customer.business_id,
                "whatsapp_number": customer.whatsapp_number,
                "display_name": customer.display_name,
                "first_seen_at": customer.first_seen_at.isoformat() if customer.first_seen_at else None,
                "last_seen_at": customer.last_seen_at.isoformat() if customer.last_seen_at else None,
            }
            for customer in customers
        ]