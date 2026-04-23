from __future__ import annotations

from app.repositories.catalog_repository import CatalogRepository
from app.schemas.catalog import CatalogBrowseResult, CatalogItemSummary


class CatalogService:
    def __init__(self, catalog_repo: CatalogRepository) -> None:
        self.catalog_repo = catalog_repo

    async def build_catalog_browse_result(self, business_id: str) -> CatalogBrowseResult:
        items = await self.catalog_repo.get_active_items(business_id)

        if not items:
            return CatalogBrowseResult(
                business_id=business_id,
                items=[],
                message="Our catalog is currently empty. Please check back later or type *help*.",
            )

        summaries = [
            CatalogItemSummary(
                id=item.id,
                name=item.name,
                description=item.description,
                price=item.price,
                currency=item.currency,
            )
            for item in items[:10]
        ]

        lines = ["🛍️ Available products:"]
        for index, item in enumerate(summaries, start=1):
            lines.append(f"{index}. {item.name} — {item.currency} {item.price}")

        lines.append("")
        lines.append("Reply with the product name to start an order.")

        return CatalogBrowseResult(
            business_id=business_id,
            items=summaries,
            message="\n".join(lines),
        )