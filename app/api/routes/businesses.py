from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.schemas.business import CreateBusinessRequest, CreateBusinessResponse
from app.schemas.business_settings import (
    BusinessSettingsResponse,
    UpsertBusinessSettingsRequest,
)
from app.schemas.business_user import CreateBusinessUserRequest, BusinessUserResponse
from app.services.setup_service import SetupService
from app.services.tenant_service import TenantService

router = APIRouter(prefix="/api/v1/businesses", tags=["Businesses"])


@router.post("", response_model=CreateBusinessResponse, summary="Create business with owner and WhatsApp account")
async def create_business(
    payload: CreateBusinessRequest,
    db: AsyncSession = Depends(get_db_session),
) -> CreateBusinessResponse:
    service = SetupService(db)
    business, owner, whatsapp_account = await service.create_business_with_owner_and_whatsapp(
        payload
    )

    return CreateBusinessResponse(
        business_id=business.id,
        business_name=business.name,
        owner_user_id=owner.id,
        whatsapp_account_id=whatsapp_account.id,
        message="Business, owner, and WhatsApp account created successfully.",
    )


@router.put(
    "/settings",
    response_model=BusinessSettingsResponse,
    summary="Create or update business settings",
)
async def upsert_business_settings(
    payload: UpsertBusinessSettingsRequest,
    db: AsyncSession = Depends(get_db_session),
) -> BusinessSettingsResponse:
    service = TenantService(db)
    result = await service.upsert_business_settings(payload)
    return BusinessSettingsResponse(**result)


@router.post(
    "/members",
    response_model=BusinessUserResponse,
    summary="Add business member",
)
async def add_business_member(
    payload: CreateBusinessUserRequest,
    db: AsyncSession = Depends(get_db_session),
) -> BusinessUserResponse:
    service = TenantService(db)
    result = await service.add_business_user(payload)
    return BusinessUserResponse(**result)