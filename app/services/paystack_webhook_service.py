from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.order_repository import OrderRepository
from app.repositories.payment_provider_repository import PaymentProviderRepository
from app.repositories.payment_repository import PaymentRepository
from app.repositories.webhook_event_repository import WebhookEventRepository
from app.services.receipt_service import ReceiptService
from app.services.webhook_security_service import WebhookSecurityService
from app.utils.encryption import decrypt_value
from app.utils.idempotency import normalize_external_event_id


class PaystackWebhookService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.payment_repo = PaymentRepository(db)
        self.order_repo = OrderRepository(db)
        self.provider_repo = PaymentProviderRepository(db)
        self.webhook_repo = WebhookEventRepository(db)
        self.receipt_service = ReceiptService(db)

    async def process_webhook(
        self,
        *,
        raw_body: bytes,
        signature_header: str | None,
        payload: dict,
    ) -> dict[str, bool]:
        data = payload.get("data") or {}
        reference = normalize_external_event_id(
            str(data.get("reference")) if data.get("reference") else None
        )

        if not reference:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing Paystack reference.",
            )

        payment = await self.payment_repo.get_by_reference(reference)
        if payment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment reference not found.",
            )

        provider = await self.provider_repo.get_active_by_business_and_provider(
            business_id=payment.business_id,
            provider="paystack",
        )
        if provider is None or not provider.secret_key_encrypted:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Active Paystack configuration not found for this business.",
            )

        secret_key = decrypt_value(provider.secret_key_encrypted)

        if not WebhookSecurityService.verify_paystack_signature(
            raw_body=raw_body,
            signature_header=signature_header,
            secret_key=secret_key,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Paystack webhook signature.",
            )

        existing_event = await self.webhook_repo.get_by_source_and_external_event_id(
            source="paystack",
            external_event_id=reference,
        )
        if existing_event is not None:
            return {"received": True}

        webhook_event = await self.webhook_repo.create(
            business_id=payment.business_id,
            source="paystack",
            external_event_id=reference,
            payload=payload,
            signature=signature_header,
        )

        event_name = payload.get("event")
        payment_status = str(data.get("status") or "").lower()

        if event_name == "charge.success" or payment_status == "success":
            await self.payment_repo.mark_paid(payment, raw_payload=payload)

            order = await self.order_repo.get_by_id(payment.order_id)
            if order is not None and order.status != "paid":
                await self.order_repo.mark_paid(order)

            await self.webhook_repo.mark_processed(webhook_event)
            await self.db.commit()
            await self.receipt_service.generate_and_deliver_receipt_for_order(payment.order_id)
            return {"received": True}

        await self.payment_repo.mark_failed(payment, raw_payload=payload)
        await self.webhook_repo.mark_processed(webhook_event)
        await self.db.commit()
        return {"received": True}