from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import Order
from app.models.order_item import OrderItem


class OrderRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_active_draft_by_customer(self, business_id: str, customer_id: str) -> Order | None:
        stmt = select(Order).where(
            Order.business_id == business_id,
            Order.customer_id == customer_id,
            Order.status == "draft",
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_latest_pending_payment_by_customer(
        self,
        business_id: str,
        customer_id: str,
    ) -> Order | None:
        stmt = (
            select(Order)
            .where(
                Order.business_id == business_id,
                Order.customer_id == customer_id,
                Order.status == "pending_payment",
            )
            .order_by(Order.updated_at.desc())
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id(self, order_id: str) -> Order | None:
        stmt = select(Order).where(Order.id == order_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_draft(
        self,
        *,
        business_id: str,
        customer_id: str,
        currency: str,
    ) -> Order:
        order = Order(
            business_id=business_id,
            customer_id=customer_id,
            currency=currency,
            status="draft",
            subtotal=Decimal("0.00"),
            total=Decimal("0.00"),
        )
        self.db.add(order)
        await self.db.flush()
        return order

    async def add_item(
        self,
        *,
        order_id: str,
        catalog_item_id: str,
        quantity: int,
        unit_price: Decimal,
    ) -> OrderItem:
        line_total = unit_price * quantity
        item = OrderItem(
            order_id=order_id,
            catalog_item_id=catalog_item_id,
            quantity=quantity,
            unit_price=unit_price,
            line_total=line_total,
        )
        self.db.add(item)
        await self.db.flush()
        return item

    async def recalculate_totals(self, order: Order) -> Order:
        stmt = select(OrderItem).where(OrderItem.order_id == order.id)
        result = await self.db.execute(stmt)
        items = list(result.scalars().all())

        subtotal = sum((item.line_total for item in items), Decimal("0.00"))
        order.subtotal = subtotal
        order.total = subtotal
        await self.db.flush()
        return order

    async def mark_pending_payment(self, order: Order) -> Order:
        order.status = "pending_payment"
        await self.db.flush()
        return order

    async def mark_paid(self, order: Order) -> Order:
        order.status = "paid"
        order.paid_at = datetime.now(UTC)
        await self.db.flush()
        return order