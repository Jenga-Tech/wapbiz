from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.customer import Customer


class CustomerRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_business_and_number(self, business_id: str, whatsapp_number: str) -> Customer | None:
        stmt = select(Customer).where(
            Customer.business_id == business_id,
            Customer.whatsapp_number == whatsapp_number,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_or_create(
        self,
        *,
        business_id: str,
        whatsapp_number: str,
        display_name: str | None,
    ) -> Customer:
        customer = await self.get_by_business_and_number(business_id, whatsapp_number)
        if customer:
            customer.display_name = display_name or customer.display_name
            customer.last_seen_at = datetime.now(UTC)
            await self.db.flush()
            return customer

        customer = Customer(
            business_id=business_id,
            whatsapp_number=whatsapp_number,
            display_name=display_name,
        )
        self.db.add(customer)
        await self.db.flush()
        return customer