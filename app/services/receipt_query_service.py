from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.receipt_repository import ReceiptRepository


class ReceiptQueryService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.receipt_repo = ReceiptRepository(db)

    async def list_receipts(self, business_id: str) -> list[dict]:
        receipts = await self.receipt_repo.list_by_business(business_id)
        return [
            {
                "id": receipt.id,
                "business_id": receipt.business_id,
                "order_id": receipt.order_id,
                "payment_id": receipt.payment_id,
                "receipt_number": receipt.receipt_number,
                "customer_delivery_status": receipt.customer_delivery_status,
                "owner_delivery_status": receipt.owner_delivery_status,
                "generated_at": receipt.generated_at.isoformat() if receipt.generated_at else None,
            }
            for receipt in receipts
        ]

    async def get_receipt_detail(self, receipt_id: str) -> dict | None:
        receipt = await self.receipt_repo.get_by_id(receipt_id)
        if receipt is None:
            return None

        return {
            "receipt_id": receipt.id,
            "receipt_number": receipt.receipt_number,
            "order_id": receipt.order_id,
            "receipt_text": receipt.receipt_text,
        }