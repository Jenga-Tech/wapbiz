from __future__ import annotations

from pydantic import BaseModel, EmailStr


class InitializePaymentRequest(BaseModel):
    order_id: str
    customer_email: EmailStr


class InitializePaymentResponse(BaseModel):
    order_id: str
    payment_reference: str
    authorization_url: str
    access_code: str | None = None
    status: str


class PaymentResponse(BaseModel):
    id: str
    business_id: str
    order_id: str
    provider: str
    provider_reference: str
    status: str
    amount: str
    currency: str
    authorization_url: str | None
    access_code: str | None
    paid_at: str | None