from functools import lru_cache
from typing import Literal

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "WapBiz API"
    app_env: Literal["development", "staging", "production"] = "development"
    app_debug: bool = True
    app_version: str = "0.1.0"
    api_v1_prefix: str = "/api/v1"

    backend_cors_origins: str = ""

    database_url: str
    database_echo: bool = False

    jwt_access_token_secret: str
    jwt_refresh_token_secret: str
    jwt_access_token_expires_minutes: int = 15
    jwt_refresh_token_expires_days: int = 30
    jwt_issuer: str = "wapbiz-api"
    jwt_audience: str = "wapbiz-dashboard"

    app_encryption_key: str

    whatsapp_verify_token: str
    whatsapp_app_secret: str | None = None
    whatsapp_access_token: str | None = None
    whatsapp_phone_number_id: str | None = None
    whatsapp_waba_id: str | None = None

    paystack_secret_key: str | None = None
    paystack_webhook_secret: str | None = None

    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def cors_origins_list(self) -> list[str]:
        if not self.backend_cors_origins.strip():
            return []

        return [
            item.strip()
            for item in self.backend_cors_origins.split(",")
            if item.strip()
        ]

    @field_validator("log_level", mode="before")
    @classmethod
    def normalize_log_level(cls, value: object) -> object:
        if isinstance(value, str):
            return value.upper().strip()
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()