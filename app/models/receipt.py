from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Receipt(Base):
    __tablename__ = "receipts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id: Mapped[str] = mapped_column(String(36), ForeignKey("businesses.id"), index=True)
    order_id: Mapped[str] = mapped_column(String(36), ForeignKey("orders.id"), index=True)
    payment_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("payments.id"), nullable=True, index=True)
    receipt_number: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    receipt_text: Mapped[str] = mapped_column(Text)
    customer_delivery_status: Mapped[str] = mapped_column(String(50), default="pending")
    owner_delivery_status: Mapped[str] = mapped_column(String(50), default="pending")
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))