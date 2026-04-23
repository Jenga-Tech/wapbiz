from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field


class UpsertBusinessSettingsRequest(BaseModel):
    business_id: str
    brand_name: str | None = Field(default=None, max_length=255)
    logo_url: str | None = None
    support_email: EmailStr | None = None
    support_phone: str | None = Field(default=None, max_length=30)
    receipt_footer: str | None = None


class BusinessSettingsResponse(BaseModel):
    business_id: str
    brand_name: str | None
    logo_url: str | None
    support_email: EmailStr | None
    support_phone: str | None
    receipt_footer: str | None