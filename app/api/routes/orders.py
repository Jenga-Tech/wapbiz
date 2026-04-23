from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.schemas.order import OrderDetailResponse, OrderResponse
from app.schemas.payment import PaymentResponse
from app.services.order_query_service import OrderQueryService
from app.services.payment_query_service import PaymentQueryService

router = APIRouter(prefix="/api/v1/orders", tags=["Orders"])


@router.get("/{business_id}", response_model=list[OrderResponse], summary="List orders for a business")
async def list_orders(
    business_id: str,
    db: AsyncSession = Depends(get_db_session),
) -> list[OrderResponse]:
    service = OrderQueryService(db)
    result = await service.list_orders(business_id)
    return [OrderResponse(**item) for item in result]


@router.get("/detail/{order_id}", response_model=OrderDetailResponse, summary="Get order details")
async def get_order_detail(
    order_id: str,
    db: AsyncSession = Depends(get_db_session),
) -> OrderDetailResponse:
    service = OrderQueryService(db)
    result = await service.get_order_detail(order_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found.",
        )
    return OrderDetailResponse(**result)


@router.get("/detail/{order_id}/payments", response_model=list[PaymentResponse], summary="List payments for an order")
async def list_order_payments(
    order_id: str,
    db: AsyncSession = Depends(get_db_session),
) -> list[PaymentResponse]:
    service = PaymentQueryService(db)
    result = await service.list_payments_for_order(order_id)
    return [PaymentResponse(**item) for item in result]