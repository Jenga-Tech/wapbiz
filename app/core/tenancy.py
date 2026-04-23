from __future__ import annotations

from fastapi import HTTPException, status

from app.core.deps import CurrentUser


def require_business_access(current_user: CurrentUser, business_id: str) -> None:
    if current_user.business_id != business_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this business.",
        )