from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import Order
from app.models.order_item import OrderItem


class OrderQueryService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def list_orders(self, business_id: str) -> list[dict]:
        result = await self.db.execute(
            select(Order).where(Order.business_id == business_id).order_by(Order.created_at.desc())
        )
        orders = list(result.scalars().all())

        return [
            {
                "id": order.id,
                "business_id": order.business_id,
                "customer_id": order.customer_id,
                "status": order.status,
                "subtotal": str(order.subtotal),
                "total": str(order.total),
                "currency": order.currency,
                "created_at": order.created_at.isoformat() if order.created_at else None,
                "paid_at": order.paid_at.isoformat() if order.paid_at else None,
            }
            for order in orders
        ]

    async def get_order_detail(self, order_id: str) -> dict | None:
        order = await self.db.scalar(select(Order).where(Order.id == order_id))
        if order is None:
            return None

        items_result = await self.db.execute(select(OrderItem).where(OrderItem.order_id == order.id))
        items = list(items_result.scalars().all())

        return {
            "id": order.id,
            "business_id": order.business_id,
            "customer_id": order.customer_id,
            "status": order.status,
            "subtotal": str(order.subtotal),
            "total": str(order.total),
            "currency": order.currency,
            "created_at": order.created_at.isoformat() if order.created_at else None,
            "paid_at": order.paid_at.isoformat() if order.paid_at else None,
            "items": [
                {
                    "id": item.id,
                    "catalog_item_id": item.catalog_item_id,
                    "quantity": item.quantity,
                    "unit_price": str(item.unit_price),
                    "line_total": str(item.line_total),
                }
                for item in items
            ],
        }