from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.schemas.customer import CustomerResponse
from app.services.customer_service import CustomerService

router = APIRouter(prefix="/api/v1/customers", tags=["Customers"])


@router.get("/{business_id}", response_model=list[CustomerResponse], summary="List customers for a business")
async def list_customers(
    business_id: str,
    db: AsyncSession = Depends(get_db_session),
) -> list[CustomerResponse]:
    service = CustomerService(db)
    result = await service.list_customers(business_id)
    return [CustomerResponse(**item) for item in result]