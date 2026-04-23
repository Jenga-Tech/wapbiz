from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, Field


class CatalogItemSummary(BaseModel):
    id: str
    name: str
    description: str | None
    price: Decimal
    currency: str


class CatalogBrowseResult(BaseModel):
    business_id: str
    items: list[CatalogItemSummary]
    message: str


class CreateCatalogItemRequest(BaseModel):
    business_id: str
    category_id: str | None = None
    external_catalog_id: str | None = None
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    price: Decimal
    currency: str = Field(default="NGN", max_length=10)
    stock_status: str = Field(default="in_stock", max_length=50)
    image_url: str | None = None
    is_active: bool = True


class UpdateCatalogItemRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    price: Decimal | None = None
    currency: str | None = Field(default=None, max_length=10)
    stock_status: str | None = Field(default=None, max_length=50)
    image_url: str | None = None
    is_active: bool | None = None


class CatalogItemResponse(BaseModel):
    id: str
    business_id: str
    category_id: str | None
    external_catalog_id: str | None
    name: str
    description: str | None
    price: str
    currency: str
    stock_status: str
    image_url: str | None
    is_active: bool