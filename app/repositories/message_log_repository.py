from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.message_log import MessageLog


class MessageLogRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(
        self,
        *,
        business_id: str,
        customer_id: str | None,
        conversation_session_id: str | None,
        direction: str,
        message_type: str,
        text_body: str | None = None,
        external_message_id: str | None = None,
        status: str | None = None,
        payload: dict | None = None,
    ) -> MessageLog:
        message_log = MessageLog(
            business_id=business_id,
            customer_id=customer_id,
            conversation_session_id=conversation_session_id,
            direction=direction,
            message_type=message_type,
            text_body=text_body,
            external_message_id=external_message_id,
            status=status,
            payload=payload,
        )
        self.db.add(message_log)
        await self.db.flush()
        return message_log