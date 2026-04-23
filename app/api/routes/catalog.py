from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.repositories.catalog_repository import CatalogRepository
from app.schemas.catalog import (
    CatalogItemResponse,
    CreateCatalogItemRequest,
    UpdateCatalogItemRequest,
)
from app.services.catalog_management_service import CatalogManagementService

router = APIRouter(prefix="/api/v1/catalog", tags=["Catalog"])


@router.get("/{business_id}/items", response_model=list[CatalogItemResponse], summary="List catalog items")
async def list_catalog_items(
    business_id: str,
    db: AsyncSession = Depends(get_db_session),
) -> list[CatalogItemResponse]:
    items = await CatalogRepository(db).get_active_items(business_id)
    return [
        CatalogItemResponse(
            id=item.id,
            business_id=item.business_id,
            category_id=item.category_id,
            external_catalog_id=item.external_catalog_id,
            name=item.name,
            description=item.description,
            price=str(item.price),
            currency=item.currency,
            stock_status=item.stock_status,
            image_url=item.image_url,
            is_active=item.is_active,
        )
        for item in items
    ]


@router.post("/items", response_model=CatalogItemResponse, summary="Create catalog item")
async def create_catalog_item(
    payload: CreateCatalogItemRequest,
    db: AsyncSession = Depends(get_db_session),
) -> CatalogItemResponse:
    service = CatalogManagementService(db)
    result = await service.create_item(payload)
    return CatalogItemResponse(**result)


@router.put("/items/{business_id}/{item_id}", response_model=CatalogItemResponse, summary="Update catalog item")
async def update_catalog_item(
    business_id: str,
    item_id: str,
    payload: UpdateCatalogItemRequest,
    db: AsyncSession = Depends(get_db_session),
) -> CatalogItemResponse:
    service = CatalogManagementService(db)
    result = await service.update_item(
        business_id=business_id,
        item_id=item_id,
        payload=payload,
    )
    return CatalogItemResponse(**result)