from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.schemas.payment import InitializePaymentRequest, InitializePaymentResponse, PaymentResponse
from app.services.payment_query_service import PaymentQueryService
from app.services.payment_service import PaymentService

router = APIRouter(prefix="/api/v1/payments", tags=["Payments"])


@router.post("/initialize", response_model=InitializePaymentResponse, summary="Initialize Paystack payment")
async def initialize_payment(
    payload: InitializePaymentRequest,
    db: AsyncSession = Depends(get_db_session),
) -> InitializePaymentResponse:
    service = PaymentService(db)
    result = await service.initialize_paystack_payment(payload)
    return InitializePaymentResponse(**result)


@router.get("/{business_id}", response_model=list[PaymentResponse], summary="List payments for a business")
async def list_payments(
    business_id: str,
    db: AsyncSession = Depends(get_db_session),
) -> list[PaymentResponse]:
    service = PaymentQueryService(db)
    result = await service.list_payments(business_id)
    return [PaymentResponse(**item) for item in result]