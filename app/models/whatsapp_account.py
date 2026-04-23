from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class WhatsAppAccount(Base):
    __tablename__ = "whatsapp_accounts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id: Mapped[str] = mapped_column(String(36), ForeignKey("businesses.id"), index=True)
    phone_number_id: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    waba_id: Mapped[str] = mapped_column(String(100), index=True)
    business_phone: Mapped[str] = mapped_column(String(30), index=True)
    verify_token: Mapped[str] = mapped_column(String(255))
    access_token_encrypted: Mapped[str | None] = mapped_column(Text, nullable=True)
    app_secret_encrypted: Mapped[str | None] = mapped_column(Text, nullable=True)
    webhook_status: Mapped[str] = mapped_column(String(50), default="pending")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )