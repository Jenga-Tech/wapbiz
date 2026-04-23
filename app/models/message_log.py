from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class MessageLog(Base):
    __tablename__ = "message_logs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id: Mapped[str] = mapped_column(String(36), ForeignKey("businesses.id"), index=True)
    customer_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("customers.id"), nullable=True, index=True)
    conversation_session_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("conversation_sessions.id"),
        nullable=True,
        index=True,
    )
    direction: Mapped[str] = mapped_column(String(20), index=True)  # inbound | outbound
    channel: Mapped[str] = mapped_column(String(30), default="whatsapp", index=True)
    external_message_id: Mapped[str | None] = mapped_column(String(150), nullable=True, index=True)
    message_type: Mapped[str] = mapped_column(String(50), index=True)
    text_body: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    payload: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))