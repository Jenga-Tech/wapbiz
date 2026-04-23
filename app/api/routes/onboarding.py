from __future__ import annotations

from fastapi import APIRouter

from app.core.config import get_settings
from app.schemas.common import MessageResponse

router = APIRouter(prefix="/api/v1/onboarding", tags=["Onboarding"])


@router.get("/status", response_model=MessageResponse, summary="Onboarding readiness status")
async def onboarding_status() -> MessageResponse:
    settings = get_settings()

    missing_items: list[str] = []

    if not settings.database_url:
        missing_items.append("database_url")
    if not settings.jwt_access_token_secret:
        missing_items.append("jwt_access_token_secret")
    if not settings.jwt_refresh_token_secret:
        missing_items.append("jwt_refresh_token_secret")
    if not settings.app_encryption_key:
        missing_items.append("app_encryption_key")
    if not settings.whatsapp_verify_token:
        missing_items.append("whatsapp_verify_token")

    if missing_items:
        return MessageResponse(
            message=f"Backend is not fully ready. Missing: {', '.join(missing_items)}"
        )

    return MessageResponse(
        message="Backend configuration looks ready for onboarding and WhatsApp integration."
    )