from __future__ import annotations

from pydantic import BaseModel, Field


class CreateBusinessUserRequest(BaseModel):
    business_id: str
    user_id: str
    role: str = Field(default="staff", max_length=50)


class BusinessUserResponse(BaseModel):
    id: str
    business_id: str
    user_id: str
    role: str