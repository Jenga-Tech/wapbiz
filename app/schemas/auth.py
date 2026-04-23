from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class TokenPairResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class AuthUserResponse(BaseModel):
    id: str
    business_id: str
    email: EmailStr
    full_name: str
    role: str
    is_active: bool


class RefreshRequest(BaseModel):
    refresh_token: str = Field(min_length=20)