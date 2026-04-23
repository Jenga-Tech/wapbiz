from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.catalog_category import CatalogCategory
from app.models.catalog_item import CatalogItem


class CatalogRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_active_categories(self, business_id: str) -> list[CatalogCategory]:
        stmt = (
            select(CatalogCategory)
            .where(
                CatalogCategory.business_id == business_id,
                CatalogCategory.is_active.is_(True),
            )
            .order_by(CatalogCategory.name.asc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_active_items(self, business_id: str) -> list[CatalogItem]:
        stmt = (
            select(CatalogItem)
            .where(
                CatalogItem.business_id == business_id,
                CatalogItem.is_active.is_(True),
            )
            .order_by(CatalogItem.name.asc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_item_by_name(self, business_id: str, item_name: str) -> CatalogItem | None:
        normalized_name = item_name.strip()
        stmt = select(CatalogItem).where(
            CatalogItem.business_id == business_id,
            CatalogItem.name.ilike(normalized_name),
            CatalogItem.is_active.is_(True),
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_item_by_id(self, business_id: str, item_id: str) -> CatalogItem | None:
        stmt = select(CatalogItem).where(
            CatalogItem.business_id == business_id,
            CatalogItem.id == item_id,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_item(
        self,
        *,
        business_id: str,
        category_id: str | None,
        external_catalog_id: str | None,
        name: str,
        description: str | None,
        price,
        currency: str,
        stock_status: str,
        image_url: str | None,
        is_active: bool,
    ) -> CatalogItem:
        item = CatalogItem(
            business_id=business_id,
            category_id=category_id,
            external_catalog_id=external_catalog_id,
            name=name,
            description=description,
            price=price,
            currency=currency,
            stock_status=stock_status,
            image_url=image_url,
            is_active=is_active,
        )
        self.db.add(item)
        await self.db.flush()
        return item

    async def update_item(
        self,
        *,
        item: CatalogItem,
        name: str | None = None,
        description: str | None = None,
        price=None,
        currency: str | None = None,
        stock_status: str | None = None,
        image_url: str | None = None,
        is_active: bool | None = None,
    ) -> CatalogItem:
        if name is not None:
            item.name = name
        if description is not None:
            item.description = description
        if price is not None:
            item.price = price
        if currency is not None:
            item.currency = currency
        if stock_status is not None:
            item.stock_status = stock_status
        if image_url is not None:
            item.image_url = image_url
        if is_active is not None:
            item.is_active = is_active

        await self.db.flush()
        return item