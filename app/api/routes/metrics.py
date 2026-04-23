from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.schemas.metrics import MetricsResponse
from app.services.metrics_service import MetricsService

router = APIRouter(prefix="/api/v1/metrics", tags=["Metrics"])


@router.get("/{business_id}", response_model=MetricsResponse, summary="Basic business metrics")
async def get_basic_metrics(
    business_id: str,
    db: AsyncSession = Depends(get_db_session),
) -> MetricsResponse:
    service = MetricsService(db)
    result = await service.get_basic_metrics(business_id)
    return MetricsResponse(**result)


@router.get("/{business_id}/summary", summary="Operational summary")
async def get_operational_summary(
    business_id: str,
    db: AsyncSession = Depends(get_db_session),
) -> dict:
    service = MetricsService(db)
    metrics = await service.get_basic_metrics(business_id)
    return {
        **metrics,
        "status": "ready",
    }