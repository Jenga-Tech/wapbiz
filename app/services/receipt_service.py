from __future__ import annotations

import uuid
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.business import Business
from app.models.catalog_item import CatalogItem
from app.models.customer import Customer
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.payment import Payment
from app.models.receipt import Receipt
from app.models.whatsapp_account import WhatsAppAccount
from app.repositories.receipt_repository import ReceiptRepository
from app.services.notification_service import NotificationService


class ReceiptService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.receipt_repo = ReceiptRepository(db)
        self.notification_service = NotificationService(db)

    async def generate_receipt_for_order(self, order_id: str) -> dict:
        existing = await self.receipt_repo.get_by_order_id(order_id)
        if existing is not None:
            return {
                "receipt_id": existing.id,
                "receipt_number": existing.receipt_number,
                "order_id": existing.order_id,
                "receipt_text": existing.receipt_text,
            }

        order = await self.db.scalar(select(Order).where(Order.id == order_id))
        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found.",
            )

        business = await self.db.scalar(select(Business).where(Business.id == order.business_id))
        customer = await self.db.scalar(select(Customer).where(Customer.id == order.customer_id))
        payment = await self.db.scalar(
            select(Payment).where(Payment.order_id == order.id).order_by(Payment.created_at.desc())
        )

        order_items_result = await self.db.execute(
            select(OrderItem, CatalogItem)
            .join(CatalogItem, CatalogItem.id == OrderItem.catalog_item_id)
            .where(OrderItem.order_id == order.id)
        )
        order_items = order_items_result.all()

        if business is None or customer is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Order relationships are incomplete.",
            )

        receipt_number = f"RCPT-{uuid.uuid4().hex[:12].upper()}"

        lines = [
            f"Receipt Number: {receipt_number}",
            f"Business: {business.name}",
            f"Order ID: {order.id}",
            f"Customer: {customer.display_name or customer.whatsapp_number}",
            f"Currency: {order.currency}",
            "",
            "Items:",
        ]

        subtotal = Decimal("0.00")
        for order_item, catalog_item in order_items:
            lines.append(
                f"- {catalog_item.name} x {order_item.quantity} = {order.currency} {order_item.line_total}"
            )
            subtotal += order_item.line_total

        lines.extend(
            [
                "",
                f"Subtotal: {order.currency} {subtotal}",
                f"Total: {order.currency} {order.total}",
                f"Payment Status: {payment.status if payment else 'pending'}",
                f"Payment Reference: {payment.provider_reference if payment else 'N/A'}",
            ]
        )

        receipt_text = "\n".join(lines)

        receipt = await self.receipt_repo.create(
            business_id=order.business_id,
            order_id=order.id,
            payment_id=payment.id if payment else None,
            receipt_number=receipt_number,
            receipt_text=receipt_text,
        )
        await self.db.commit()

        return {
            "receipt_id": receipt.id,
            "receipt_number": receipt.receipt_number,
            "order_id": receipt.order_id,
            "receipt_text": receipt.receipt_text,
        }

    async def generate_and_deliver_receipt_for_order(self, order_id: str) -> dict:
        result = await self.generate_receipt_for_order(order_id)

        order = await self.db.scalar(select(Order).where(Order.id == order_id))
        customer = await self.db.scalar(select(Customer).where(Customer.id == order.customer_id))
        receipt = await self.receipt_repo.get_by_order_id(order_id)
        whatsapp_account = await self.db.scalar(
            select(WhatsAppAccount).where(WhatsAppAccount.business_id == order.business_id)
        )
        business = await self.db.scalar(select(Business).where(Business.id == order.business_id))

        if receipt and customer and whatsapp_account:
            await self.notification_service.send_text_to_customer(
                business_id=order.business_id,
                customer_id=customer.id,
                conversation_session_id=None,
                to=customer.whatsapp_number,
                body=receipt.receipt_text,
                phone_number_id=whatsapp_account.phone_number_id,
            )
            await self.notification_service.mark_receipt_customer_delivered(receipt)

        if receipt and business and business.contact_phone and whatsapp_account:
            await self.notification_service.send_text_to_customer(
                business_id=order.business_id,
                customer_id=None,
                conversation_session_id=None,
                to=business.contact_phone,
                body=f"New paid order receipt\n\n{receipt.receipt_text}",
                phone_number_id=whatsapp_account.phone_number_id,
            )
            await self.notification_service.mark_receipt_owner_delivered(receipt)

        await self.db.commit()
        return result