from __future__ import annotations

from pydantic import BaseModel


class OrderItemResponse(BaseModel):
    id: str
    catalog_item_id: str
    quantity: int
    unit_price: str
    line_total: str


class OrderResponse(BaseModel):
    id: str
    business_id: str
    customer_id: str
    status: str
    subtotal: str
    total: str
    currency: str
    created_at: str | None
    paid_at: str | None


class OrderDetailResponse(OrderResponse):
    items: list[OrderItemResponse]