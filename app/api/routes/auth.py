from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.core.deps import CurrentUser, get_current_user
from app.repositories.user_repository import UserRepository
from app.schemas.auth import AuthUserResponse, LoginRequest, RefreshRequest, TokenPairResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])


@router.post("/login", response_model=TokenPairResponse)
async def login(
    payload: LoginRequest,
    request: Request,
    db: AsyncSession = Depends(get_db_session),
) -> TokenPairResponse:
    service = AuthService(db)
    tokens = await service.login(
        email=payload.email,
        password=payload.password,
        user_agent=request.headers.get("user-agent"),
        ip_address=request.client.host if request.client else None,
    )
    return TokenPairResponse(**tokens)


@router.post("/refresh", response_model=TokenPairResponse)
async def refresh(
    payload: RefreshRequest,
    db: AsyncSession = Depends(get_db_session),
) -> TokenPairResponse:
    service = AuthService(db)
    tokens = await service.refresh_tokens(refresh_token=payload.refresh_token)
    return TokenPairResponse(**tokens)


@router.get("/me", response_model=AuthUserResponse)
async def me(
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> AuthUserResponse:
    user = await UserRepository(db).get_by_id(current_user.id)
    return AuthUserResponse(
        id=user.id,
        business_id=user.business_id,
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        is_active=user.is_active,
    )