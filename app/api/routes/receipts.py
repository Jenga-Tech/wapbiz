from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.schemas.receipt import ReceiptListItemResponse, ReceiptResponse
from app.services.receipt_query_service import ReceiptQueryService
from app.services.receipt_service import ReceiptService

router = APIRouter(prefix="/api/v1/receipts", tags=["Receipts"])


@router.post("/{order_id}/generate", response_model=ReceiptResponse, summary="Generate receipt for order")
async def generate_receipt(
    order_id: str,
    db: AsyncSession = Depends(get_db_session),
) -> ReceiptResponse:
    service = ReceiptService(db)
    result = await service.generate_receipt_for_order(order_id)
    return ReceiptResponse(**result)


@router.get("/{business_id}", response_model=list[ReceiptListItemResponse], summary="List receipts for a business")
async def list_receipts(
    business_id: str,
    db: AsyncSession = Depends(get_db_session),
) -> list[ReceiptListItemResponse]:
    service = ReceiptQueryService(db)
    result = await service.list_receipts(business_id)
    return [ReceiptListItemResponse(**item) for item in result]


@router.get("/detail/{receipt_id}", response_model=ReceiptResponse, summary="Get receipt detail")
async def get_receipt_detail(
    receipt_id: str,
    db: AsyncSession = Depends(get_db_session),
) -> ReceiptResponse:
    service = ReceiptQueryService(db)
    result = await service.get_receipt_detail(receipt_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receipt not found.",
        )
    return ReceiptResponse(**result)