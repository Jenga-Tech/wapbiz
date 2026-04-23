from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.conversation_session_repository import ConversationSessionRepository


class ConversationQueryService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.session_repo = ConversationSessionRepository(db)

    async def list_sessions(self, business_id: str) -> list[dict]:
        sessions = await self.session_repo.list_by_business(business_id)

        results: list[dict] = []
        for session in sessions:
            context_json = session.context_json or {}
            results.append(
                {
                    "id": session.id,
                    "business_id": session.business_id,
                    "customer_id": session.customer_id,
                    "current_state": session.current_state,
                    "last_incoming_message_id": session.last_incoming_message_id,
                    "last_outgoing_message_id": session.last_outgoing_message_id,
                    "last_message_at": session.last_message_at.isoformat()
                    if session.last_message_at
                    else None,
                    "expires_at": session.expires_at.isoformat() if session.expires_at else None,
                    "human_handoff_requested": bool(
                        context_json.get("human_handoff_requested", False)
                    ),
                }
            )
        return results