from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.conversation_session import ConversationSession


class ConversationSessionRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_business_and_customer(
        self,
        *,
        business_id: str,
        customer_id: str,
    ) -> ConversationSession | None:
        stmt = select(ConversationSession).where(
            ConversationSession.business_id == business_id,
            ConversationSession.customer_id == customer_id,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_business(self, business_id: str) -> list[ConversationSession]:
        stmt = (
            select(ConversationSession)
            .where(ConversationSession.business_id == business_id)
            .order_by(ConversationSession.last_message_at.desc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_or_create(
        self,
        *,
        business_id: str,
        customer_id: str,
    ) -> ConversationSession:
        session = await self.get_by_business_and_customer(
            business_id=business_id,
            customer_id=customer_id,
        )
        if session:
            session.last_message_at = datetime.now(UTC)
            await self.db.flush()
            return session

        session = ConversationSession(
            business_id=business_id,
            customer_id=customer_id,
        )
        self.db.add(session)
        await self.db.flush()
        return session

    async def update_state(
        self,
        *,
        session: ConversationSession,
        current_state: str,
        context_json: dict | None = None,
        cart_json: dict | None = None,
        last_incoming_message_id: str | None = None,
        last_outgoing_message_id: str | None = None,
    ) -> ConversationSession:
        session.current_state = current_state
        session.last_message_at = datetime.now(UTC)

        if context_json is not None:
            session.context_json = context_json
        if cart_json is not None:
            session.cart_json = cart_json
        if last_incoming_message_id is not None:
            session.last_incoming_message_id = last_incoming_message_id
        if last_outgoing_message_id is not None:
            session.last_outgoing_message_id = last_outgoing_message_id

        await self.db.flush()
        return session