from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.receipt import Receipt


class ReceiptRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_order_id(self, order_id: str) -> Receipt | None:
        stmt = select(Receipt).where(Receipt.order_id == order_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id(self, receipt_id: str) -> Receipt | None:
        stmt = select(Receipt).where(Receipt.id == receipt_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_business(self, business_id: str) -> list[Receipt]:
        stmt = select(Receipt).where(Receipt.business_id == business_id).order_by(Receipt.generated_at.desc())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(
        self,
        *,
        business_id: str,
        order_id: str,
        payment_id: str | None,
        receipt_number: str,
        receipt_text: str,
    ) -> Receipt:
        receipt = Receipt(
            business_id=business_id,
            order_id=order_id,
            payment_id=payment_id,
            receipt_number=receipt_number,
            receipt_text=receipt_text,
        )
        self.db.add(receipt)
        await self.db.flush()
        return receipt