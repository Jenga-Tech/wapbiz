from __future__ import annotations

from pydantic import BaseModel


class ReceiptResponse(BaseModel):
    receipt_id: str
    receipt_number: str
    order_id: str
    receipt_text: str


class ReceiptListItemResponse(BaseModel):
    id: str
    business_id: str
    order_id: str
    payment_id: str | None
    receipt_number: str
    customer_delivery_status: str
    owner_delivery_status: str
    generated_at: str | None