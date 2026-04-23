from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.catalog_repository import CatalogRepository
from app.repositories.order_repository import OrderRepository


class OrderService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.catalog_repo = CatalogRepository(db)
        self.order_repo = OrderRepository(db)

    async def create_or_update_draft_order_from_item_name(
        self,
        *,
        business_id: str,
        customer_id: str,
        item_name: str,
        quantity: int = 1,
    ) -> dict:
        catalog_item = await self.catalog_repo.get_item_by_name(business_id, item_name)
        if catalog_item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Catalog item not found.",
            )

        order = await self.order_repo.get_active_draft_by_customer(business_id, customer_id)
        if order is None:
            order = await self.order_repo.create_draft(
                business_id=business_id,
                customer_id=customer_id,
                currency=catalog_item.currency,
            )

        await self.order_repo.add_item(
            order_id=order.id,
            catalog_item_id=catalog_item.id,
            quantity=quantity,
            unit_price=catalog_item.price,
        )
        order = await self.order_repo.recalculate_totals(order)

        await self.db.flush()

        return {
            "order_id": order.id,
            "status": order.status,
            "currency": order.currency,
            "subtotal": str(order.subtotal),
            "item_name": catalog_item.name,
            "quantity": quantity,
        }