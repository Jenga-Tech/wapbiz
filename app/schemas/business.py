from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field, field_validator


class CreateBusinessRequest(BaseModel):
    business_name: str = Field(min_length=2, max_length=255)
    business_slug: str = Field(min_length=2, max_length=120)
    contact_email: EmailStr | None = None
    contact_phone: str | None = Field(default=None, max_length=30)
    country: str | None = Field(default=None, max_length=100)
    currency: str = Field(default="NGN", max_length=10)
    timezone: str = Field(default="Africa/Lagos", max_length=100)

    owner_full_name: str = Field(min_length=2, max_length=255)
    owner_email: EmailStr
    owner_password: str = Field(min_length=8, max_length=128)

    whatsapp_phone_number_id: str = Field(min_length=2, max_length=100)
    whatsapp_waba_id: str = Field(min_length=2, max_length=100)
    whatsapp_business_phone: str = Field(min_length=5, max_length=30)
    whatsapp_verify_token: str = Field(min_length=6, max_length=255)
    whatsapp_access_token: str = Field(min_length=10)
    whatsapp_app_secret: str | None = Field(default=None, min_length=10)

    @field_validator("business_slug", mode="before")
    @classmethod
    def normalize_business_slug(cls, value: object) -> object:
        if isinstance(value, str):
            return value.strip().lower().replace(" ", "-")
        return value

    @field_validator(
        "business_name",
        "owner_full_name",
        "whatsapp_business_phone",
        "whatsapp_phone_number_id",
        "whatsapp_waba_id",
        "whatsapp_verify_token",
        mode="before",
    )
    @classmethod
    def strip_string_fields(cls, value: object) -> object:
        if isinstance(value, str):
            return value.strip()
        return value


class CreateBusinessResponse(BaseModel):
    business_id: str
    business_name: str
    owner_user_id: str
    whatsapp_account_id: str
    message: str