from __future__ import annotations

from pydantic import BaseModel


class IncomingWhatsAppMessage(BaseModel):
    business_id: str
    phone_number_id: str
    customer_number: str
    customer_name: str | None = None
    message_id: str
    message_type: str
    text_body: str | None = None
    raw_payload: dict


class ConversationSessionResponse(BaseModel):
    id: str
    business_id: str
    customer_id: str
    current_state: str
    last_incoming_message_id: str | None
    last_outgoing_message_id: str | None
    last_message_at: str | None
    expires_at: str | None
    human_handoff_requested: bool = False