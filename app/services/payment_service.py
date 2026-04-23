from __future__ import annotations

import uuid
from decimal import Decimal, ROUND_HALF_UP

import httpx
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.order_repository import OrderRepository
from app.repositories.payment_provider_repository import PaymentProviderRepository
from app.repositories.payment_repository import PaymentRepository
from app.schemas.payment import InitializePaymentRequest
from app.utils.encryption import decrypt_value


class PaymentService:
    PAYSTACK_INITIALIZE_URL = "https://api.paystack.co/transaction/initialize"

    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.order_repo = OrderRepository(db)
        self.provider_repo = PaymentProviderRepository(db)
        self.payment_repo = PaymentRepository(db)

    async def initialize_paystack_payment(
        self,
        payload: InitializePaymentRequest,
    ) -> dict:
        order = await self.order_repo.get_by_id(payload.order_id)
        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found.",
            )

        if order.total <= Decimal("0.00"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Order total must be greater than zero before payment initialization.",
            )

        provider = await self.provider_repo.get_active_by_business_and_provider(
            business_id=order.business_id,
            provider="paystack",
        )
        if provider is None or not provider.secret_key_encrypted:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Active Paystack configuration not found for this business.",
            )

        secret_key = decrypt_value(provider.secret_key_encrypted)
        reference = f"wapbiz-{order.id}-{uuid.uuid4().hex[:10]}"

        normalized_total = order.total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        amount_kobo = int(normalized_total * 100)

        request_payload = {
            "email": payload.customer_email,
            "amount": amount_kobo,
            "reference": reference,
            "currency": order.currency,
            "metadata": {
                "business_id": order.business_id,
                "order_id": order.id,
            },
        }

        headers = {
            "Authorization": f"Bearer {secret_key}",
            "Content-Type": "application/json",
        }

        try:
            async with httpx.AsyncClient(timeout=20.0) as client:
                response = await client.post(
                    self.PAYSTACK_INITIALIZE_URL,
                    headers=headers,
                    json=request_payload,
                )
                response.raise_for_status()
                provider_response = response.json()
        except httpx.HTTPError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Unable to initialize Paystack payment at this time.",
            ) from exc

        data = provider_response.get("data") or {}
        authorization_url = data.get("authorization_url")
        access_code = data.get("access_code")

        if not authorization_url:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Payment provider did not return an authorization URL.",
            )

        await self.payment_repo.create(
            business_id=order.business_id,
            order_id=order.id,
            provider="paystack",
            provider_reference=reference,
            amount=order.total,
            currency=order.currency,
            authorization_url=authorization_url,
            access_code=access_code,
            raw_payload=provider_response,
        )
        await self.order_repo.mark_pending_payment(order)
        await self.db.commit()

        return {
            "order_id": order.id,
            "payment_reference": reference,
            "authorization_url": authorization_url,
            "access_code": access_code,
            "status": "initialized",
        }