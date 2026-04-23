from __future__ import annotations

from pydantic import BaseModel


class OutboundWhatsAppTextMessage(BaseModel):
    business_id: str
    to: str
    body: str