from __future__ import annotations

from pydantic import BaseModel


class CustomerResponse(BaseModel):
    id: str
    business_id: str
    whatsapp_number: str
    display_name: str | None
    first_seen_at: str | None
    last_seen_at: str | None