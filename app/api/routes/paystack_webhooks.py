from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.services.paystack_webhook_service import PaystackWebhookService

router = APIRouter(tags=["Paystack Webhooks"])


@router.post("/webhook/paystack", summary="Inbound Paystack events")
async def receive_paystack_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db_session),
) -> dict[str, bool]:
    raw_body = await request.body()
    payload = await request.json()
    signature_header = request.headers.get("x-paystack-signature")

    service = PaystackWebhookService(db)
    return await service.process_webhook(
        raw_body=raw_body,
        signature_header=signature_header,
        payload=payload,
    )