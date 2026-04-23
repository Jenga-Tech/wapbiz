from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.webhook_event import WebhookEvent


class WebhookEventRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_source_and_external_event_id(
        self,
        *,
        source: str,
        external_event_id: str,
    ) -> WebhookEvent | None:
        stmt = select(WebhookEvent).where(
            WebhookEvent.source == source,
            WebhookEvent.external_event_id == external_event_id,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(
        self,
        *,
        business_id: str | None,
        source: str,
        external_event_id: str | None,
        payload: dict,
        signature: str | None = None,
    ) -> WebhookEvent:
        event = WebhookEvent(
            business_id=business_id,
            source=source,
            external_event_id=external_event_id,
            payload=payload,
            signature=signature,
        )
        self.db.add(event)
        await self.db.flush()
        return event

    async def mark_processed(self, event: WebhookEvent) -> None:
        event.processed = True
        event.processed_at = datetime.now(UTC)
        await self.db.flush()