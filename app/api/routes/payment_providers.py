from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.schemas.payment_provider import (
    CreatePaymentProviderRequest,
    CreatePaymentProviderResponse,
)
from app.services.payment_provider_service import PaymentProviderService

router = APIRouter(prefix="/api/v1/payment-providers", tags=["Payment Providers"])


@router.post("", response_model=CreatePaymentProviderResponse, summary="Create payment provider")
async def create_payment_provider(
    payload: CreatePaymentProviderRequest,
    db: AsyncSession = Depends(get_db_session),
) -> CreatePaymentProviderResponse:
    service = PaymentProviderService(db)
    result = await service.create_payment_provider(payload)
    return CreatePaymentProviderResponse(**result)