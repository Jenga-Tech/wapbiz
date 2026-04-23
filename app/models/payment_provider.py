from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class PaymentProvider(Base):
    __tablename__ = "payment_providers"
    __table_args__ = (
        UniqueConstraint("business_id", "provider", name="uq_payment_providers_business_provider"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id: Mapped[str] = mapped_column(String(36), ForeignKey("businesses.id"), index=True)
    provider: Mapped[str] = mapped_column(String(50), index=True)  # paystack, stripe later
    public_key_encrypted: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    secret_key_encrypted: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    webhook_secret_encrypted: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )