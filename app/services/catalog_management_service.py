from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.business_repository import BusinessRepository
from app.repositories.catalog_repository import CatalogRepository
from app.schemas.catalog import CreateCatalogItemRequest, UpdateCatalogItemRequest


class CatalogManagementService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.business_repo = BusinessRepository(db)
        self.catalog_repo = CatalogRepository(db)

    async def create_item(self, payload: CreateCatalogItemRequest) -> dict:
        business = await self.business_repo.get_by_id(payload.business_id)
        if business is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Business not found.",
            )

        item = await self.catalog_repo.create_item(
            business_id=payload.business_id,
            category_id=payload.category_id,
            external_catalog_id=payload.external_catalog_id,
            name=payload.name.strip(),
            description=payload.description,
            price=payload.price,
            currency=payload.currency.upper(),
            stock_status=payload.stock_status,
            image_url=payload.image_url,
            is_active=payload.is_active,
        )
        await self.db.commit()

        return {
            "id": item.id,
            "business_id": item.business_id,
            "category_id": item.category_id,
            "external_catalog_id": item.external_catalog_id,
            "name": item.name,
            "description": item.description,
            "price": str(item.price),
            "currency": item.currency,
            "stock_status": item.stock_status,
            "image_url": item.image_url,
            "is_active": item.is_active,
        }

    async def update_item(
        self,
        *,
        business_id: str,
        item_id: str,
        payload: UpdateCatalogItemRequest,
    ) -> dict:
        item = await self.catalog_repo.get_item_by_id(business_id, item_id)
        if item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Catalog item not found.",
            )

        item = await self.catalog_repo.update_item(
            item=item,
            name=payload.name.strip() if payload.name is not None else None,
            description=payload.description,
            price=payload.price,
            currency=payload.currency.upper() if payload.currency is not None else None,
            stock_status=payload.stock_status,
            image_url=payload.image_url,
            is_active=payload.is_active,
        )
        await self.db.commit()

        return {
            "id": item.id,
            "business_id": item.business_id,
            "category_id": item.category_id,
            "external_catalog_id": item.external_catalog_id,
            "name": item.name,
            "description": item.description,
            "price": str(item.price),
            "currency": item.currency,
            "stock_status": item.stock_status,
            "image_url": item.image_url,
            "is_active": item.is_active,
        }