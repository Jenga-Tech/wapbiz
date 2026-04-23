from __future__ import annotations

from pydantic import BaseModel, Field


class CreatePaymentProviderRequest(BaseModel):
    business_id: str
    provider: str = Field(default="paystack", max_length=50)
    public_key: str | None = None
    secret_key: str
    webhook_secret: str | None = None


class CreatePaymentProviderResponse(BaseModel):
    payment_provider_id: str
    business_id: str
    provider: str
    message: str