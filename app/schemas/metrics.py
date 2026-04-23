from __future__ import annotations

from pydantic import BaseModel


class MetricsResponse(BaseModel):
    business_id: str
    customers: int
    orders: int
    paid_payments: int
    receipts: int