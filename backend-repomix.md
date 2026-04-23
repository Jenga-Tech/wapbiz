This file is a merged representation of the entire codebase, combined into a single document by Repomix.

<file_summary>
This section contains a summary of this file.

<purpose>
This file contains a packed representation of the entire repository's contents.
It is designed to be easily consumable by AI systems for analysis, code review,
or other automated processes.
</purpose>

<file_format>
The content is organized as follows:
1. This summary section
2. Repository information
3. Directory structure
4. Repository files (if enabled)
5. Multiple file entries, each consisting of:
  - File path as an attribute
  - Full contents of the file
</file_format>

<usage_guidelines>
- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.
</usage_guidelines>

<notes>
- Some files may have been excluded based on .gitignore rules and Repomix's configuration
- Binary files are not included in this packed representation. Please refer to the Repository Structure section for a complete list of file paths, including binary files
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Files are sorted by Git change count (files with more changes are at the bottom)
</notes>

</file_summary>

<directory_structure>
.gitignore
alembic.ini
alembic/env.py
alembic/script.py.mako
app/__init__.py
app/api/__init__.py
app/api/routes/__init__.py
app/api/routes/auth.py
app/api/routes/businesses.py
app/api/routes/catalog.py
app/api/routes/customers.py
app/api/routes/health.py
app/api/routes/metrics.py
app/api/routes/onboarding.py
app/api/routes/orders.py
app/api/routes/payment_providers.py
app/api/routes/payments.py
app/api/routes/paystack_webhooks.py
app/api/routes/receipts.py
app/api/routes/whatsapp_webhooks.py
app/core/__init__.py
app/core/config.py
app/core/constants.py
app/core/database.py
app/core/deps.py
app/core/logging.py
app/core/security.py
app/core/tenancy.py
app/main.py
app/models/__init__.py
app/models/audit_log.py
app/models/base.py
app/models/business_settings.py
app/models/business_user.py
app/models/business.py
app/models/catalog_category.py
app/models/catalog_item.py
app/models/conversation_session.py
app/models/customer.py
app/models/message_log.py
app/models/order_item.py
app/models/order.py
app/models/payment_provider.py
app/models/payment.py
app/models/receipt.py
app/models/user_session.py
app/models/user.py
app/models/webhook_event.py
app/models/whatsapp_account.py
app/repositories/__init__.py
app/repositories/audit_log_repository.py
app/repositories/base.py
app/repositories/business_repository.py
app/repositories/business_settings_repository.py
app/repositories/business_user_repository.py
app/repositories/catalog_repository.py
app/repositories/conversation_session_repository.py
app/repositories/customer_repository.py
app/repositories/message_log_repository.py
app/repositories/order_repository.py
app/repositories/payment_provider_repository.py
app/repositories/payment_repository.py
app/repositories/receipt_repository.py
app/repositories/setup_repository.py
app/repositories/user_repository.py
app/repositories/user_session_repository.py
app/repositories/webhook_event_repository.py
app/repositories/whatsapp_account_repository.py
app/schemas/__init__.py
app/schemas/auth.py
app/schemas/business_settings.py
app/schemas/business_user.py
app/schemas/business.py
app/schemas/catalog.py
app/schemas/common.py
app/schemas/customer.py
app/schemas/metrics.py
app/schemas/order.py
app/schemas/outbound_whatsapp.py
app/schemas/payment_provider.py
app/schemas/payment.py
app/schemas/paystack.py
app/schemas/receipt.py
app/schemas/whatsapp.py
app/services/__init__.py
app/services/audit_service.py
app/services/auth_service.py
app/services/catalog_service.py
app/services/conversation_service.py
app/services/customer_service.py
app/services/metrics_service.py
app/services/notification_service.py
app/services/onboarding_service.py
app/services/order_service.py
app/services/payment_provider_service.py
app/services/payment_service.py
app/services/receipt_service.py
app/services/setup_service.py
app/services/tenant_service.py
app/services/webhook_security_service.py
app/services/whatsapp_reply_service.py
app/services/whatsapp_service.py
app/services/whatsapp_webhook_service.py
app/tests/__init__.py
app/tests/conftest.py
app/tests/test_auth.py
app/tests/test_health.py
app/tests/test_onboarding_status.py
app/tests/test_orders.py
app/tests/test_paystack_webhook.py
app/tests/test_whatsapp_webhook.py
app/utils/__init__.py
app/utils/encryption.py
app/utils/exceptions.py
app/utils/formatting.py
app/utils/idempotency.py
app/utils/pagination.py
app/utils/time.py
app/workers/__init__.py
app/workers/catalog_sync_jobs.py
app/workers/notification_jobs.py
app/workers/receipt_jobs.py
app/workers/retry_jobs.py
backend_setup.sh
docker-compose.yml
Dockerfile
pyproject.toml
README.md
requirements.txt
</directory_structure>

<files>
This section contains the contents of the repository's files.

<file path=".gitignore">
# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd

# Virtual environments
.venv/
venv/

# Environment files
.env
.env.*

# Tooling caches
.pytest_cache/
.ruff_cache/
.mypy_cache/
.coverage
htmlcov/

# IDE / OS
.vscode/
.idea/
.DS_Store
Thumbs.db

# Alembic compiled files
alembic/versions/*.pyc
</file>

<file path="alembic.ini">
[alembic]
script_location = alembic
prepend_sys_path = .
sqlalchemy.url = postgresql+psycopg://postgres:postgres@localhost:5432/wapbiz

[post_write_hooks]

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers = console
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
</file>

<file path="alembic/env.py">
from __future__ import annotations

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.core.database import get_sync_database_url
from app.models import Base  # noqa: F401
from app.models import (  # noqa: F401
    Business,
    CatalogCategory,
    CatalogItem,
    ConversationSession,
    Customer,
    MessageLog,
    Order,
    OrderItem,
    Payment,
    PaymentProvider,
    Receipt,
    User,
    UserSession,
    WebhookEvent,
    WhatsAppAccount,
)

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

config.set_main_option("sqlalchemy.url", get_sync_database_url())

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
</file>

<file path="alembic/script.py.mako">
"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa

${imports if imports else ""}


# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade() -> None:
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    ${downgrades if downgrades else "pass"}
</file>

<file path="app/__init__.py">

</file>

<file path="app/api/__init__.py">

</file>

<file path="app/api/routes/__init__.py">

</file>

<file path="app/api/routes/auth.py">
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
</file>

<file path="app/api/routes/businesses.py">
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.schemas.business import CreateBusinessRequest, CreateBusinessResponse
from app.services.setup_service import SetupService

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
</file>

<file path="app/api/routes/catalog.py">

</file>

<file path="app/api/routes/customers.py">

</file>

<file path="app/api/routes/health.py">
from fastapi import APIRouter

from app.core.config import get_settings
from app.schemas.common import HealthResponse

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse, summary="Health check")
async def health_check() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(
        status="ok",
        service=settings.app_name,
        environment=settings.app_env,
        version=settings.app_version,
    )
</file>

<file path="app/api/routes/metrics.py">

</file>

<file path="app/api/routes/onboarding.py">
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
</file>

<file path="app/api/routes/orders.py">

</file>

<file path="app/api/routes/payment_providers.py">
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.schemas.payment_provider import (
    CreatePaymentProviderRequest,
    CreatePaymentProviderResponse,
)
from app.services.payment_provider_service import PaymentProviderService

router = APIRouter(prefix="/api/v1/payment-providers", tags=["Payment Providers"])


@router.post("", response_model=CreatePaymentProviderResponse, summary="Create payment provider")
async def create_payment_provider(
    payload: CreatePaymentProviderRequest,
    db: AsyncSession = Depends(get_db_session),
) -> CreatePaymentProviderResponse:
    service = PaymentProviderService(db)
    result = await service.create_payment_provider(payload)
    return CreatePaymentProviderResponse(**result)
</file>

<file path="app/api/routes/payments.py">
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.schemas.payment import InitializePaymentRequest, InitializePaymentResponse
from app.services.payment_service import PaymentService

router = APIRouter(prefix="/api/v1/payments", tags=["Payments"])


@router.post("/initialize", response_model=InitializePaymentResponse, summary="Initialize Paystack payment")
async def initialize_payment(
    payload: InitializePaymentRequest,
    db: AsyncSession = Depends(get_db_session),
) -> InitializePaymentResponse:
    service = PaymentService(db)
    result = await service.initialize_paystack_payment(payload)
    return InitializePaymentResponse(**result)
</file>

<file path="app/api/routes/paystack_webhooks.py">
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.database import get_db_session
from app.repositories.webhook_event_repository import WebhookEventRepository
from app.services.webhook_security_service import WebhookSecurityService
from app.utils.idempotency import normalize_external_event_id

router = APIRouter(tags=["Paystack Webhooks"])
settings = get_settings()


@router.post("/webhook/paystack", summary="Inbound Paystack events")
async def receive_paystack_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db_session),
) -> dict[str, bool]:
    raw_body = await request.body()
    signature_header = request.headers.get("x-paystack-signature")

    if not WebhookSecurityService.verify_paystack_signature(
        raw_body=raw_body,
        signature_header=signature_header,
        secret_key=settings.paystack_secret_key,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Paystack webhook signature.",
        )

    payload = await request.json()
    data = payload.get("data") or {}
    external_event_id = normalize_external_event_id(
        str(data.get("reference")) if data.get("reference") else None
    )

    repo = WebhookEventRepository(db)

    if external_event_id:
        existing = await repo.get_by_source_and_external_event_id(
            source="paystack",
            external_event_id=external_event_id,
        )
        if existing is not None:
            return {"received": True}

    await repo.create(
        business_id=None,
        source="paystack",
        external_event_id=external_event_id,
        payload=payload,
        signature=signature_header,
    )
    await db.commit()

    return {"received": True}
</file>

<file path="app/api/routes/receipts.py">
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.schemas.receipt import ReceiptResponse
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
</file>

<file path="app/api/routes/whatsapp_webhooks.py">
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.database import get_db_session
from app.repositories.business_repository import BusinessRepository
from app.repositories.message_log_repository import MessageLogRepository
from app.repositories.webhook_event_repository import WebhookEventRepository
from app.repositories.whatsapp_account_repository import WhatsAppAccountRepository
from app.services.conversation_service import ConversationService
from app.services.webhook_security_service import WebhookSecurityService
from app.services.whatsapp_service import WhatsAppService
from app.services.whatsapp_webhook_service import WhatsAppWebhookService

router = APIRouter(tags=["WhatsApp Webhooks"])
settings = get_settings()


@router.get("/webhook/whatsapp", summary="Meta webhook verification")
async def verify_whatsapp_webhook(
    hub_mode: str = Query(alias="hub.mode"),
    hub_verify_token: str = Query(alias="hub.verify_token"),
    hub_challenge: str = Query(alias="hub.challenge"),
    db: AsyncSession = Depends(get_db_session),
) -> Response:
    if hub_mode != "subscribe":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Webhook verification failed.",
        )

    whatsapp_account = await WhatsAppAccountRepository(db).get_by_verify_token(hub_verify_token)

    is_valid = whatsapp_account is not None
    if not is_valid and hub_verify_token == settings.whatsapp_verify_token:
        is_valid = True

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Webhook verification failed.",
        )

    return Response(content=hub_challenge, media_type="text/plain")


@router.post("/webhook/whatsapp", summary="Inbound WhatsApp events")
async def receive_whatsapp_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db_session),
) -> dict[str, bool | int]:
    raw_body = await request.body()
    payload = await request.json()

    entry_list = payload.get("entry", [])
    external_event_id = None
    phone_number_id = None

    if entry_list:
        external_event_id = str(entry_list[0].get("id", "")) or None

    for entry in entry_list:
        for change in entry.get("changes", []):
            value = change.get("value", {})
            metadata = value.get("metadata", {})
            phone_number_id = metadata.get("phone_number_id")
            if phone_number_id:
                break
        if phone_number_id:
            break

    whatsapp_account = None
    if phone_number_id:
        whatsapp_account = await WhatsAppAccountRepository(db).get_by_phone_number_id(phone_number_id)

    signature_header = request.headers.get("X-Hub-Signature-256")
    if whatsapp_account is None or not WebhookSecurityService.verify_meta_signature(
        raw_body=raw_body,
        signature_header=signature_header,
        app_secret_encrypted=whatsapp_account.app_secret_encrypted,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid WhatsApp webhook signature.",
        )

    webhook_repo = WebhookEventRepository(db)
    existing_event = None
    if external_event_id:
        existing_event = await webhook_repo.get_by_source_and_external_event_id(
            source="meta",
            external_event_id=external_event_id,
        )

    if existing_event is not None:
        return {"received": True, "processed_messages": 0}

    webhook_event = await webhook_repo.create(
        business_id=whatsapp_account.business_id if whatsapp_account else None,
        source="meta",
        external_event_id=external_event_id,
        payload=payload,
        signature=signature_header,
    )

    whatsapp_webhook_service = WhatsAppWebhookService(WhatsAppAccountRepository(db))
    normalized_messages = await whatsapp_webhook_service.extract_messages(payload)

    conversation_service = ConversationService(db)
    business_repo = BusinessRepository(db)
    message_log_repo = MessageLogRepository(db)
    whatsapp_service = WhatsAppService()

    processed_count = 0

    for message in normalized_messages:
        result = await conversation_service.handle_incoming_message(message)

        business, whatsapp_account = await business_repo.get_business_and_whatsapp_account(
            result["phone_number_id"]
        )

        if (
            business is not None
            and whatsapp_account is not None
            and whatsapp_account.access_token_encrypted
            and result["reply_text"]
        ):
            provider_response = await whatsapp_service.send_text_message(
                access_token_encrypted=whatsapp_account.access_token_encrypted,
                phone_number_id=result["phone_number_id"],
                to=result["customer_number"],
                body=result["reply_text"],
            )

            outbound_message_id = None
            messages = provider_response.get("messages") or []
            if messages:
                outbound_message_id = messages[0].get("id")

            await message_log_repo.create(
                business_id=result["business_id"],
                customer_id=result["customer_id"],
                conversation_session_id=result["session_id"],
                direction="outbound",
                message_type="text",
                text_body=result["reply_text"],
                external_message_id=outbound_message_id,
                status="sent",
                payload=provider_response,
            )

        processed_count += 1

    await webhook_repo.mark_processed(webhook_event)
    await db.commit()

    return {
        "received": True,
        "processed_messages": processed_count,
    }
</file>

<file path="app/core/__init__.py">

</file>

<file path="app/core/config.py">
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
</file>

<file path="app/core/constants.py">

</file>

<file path="app/core/database.py">
from collections.abc import AsyncGenerator

from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import get_settings

settings = get_settings()

engine: AsyncEngine = create_async_engine(
    settings.database_url,
    echo=settings.database_echo,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


def get_sync_database_url() -> str:
    """
    Alembic runs with a synchronous engine.
    Convert SQLAlchemy async URLs like `postgresql+psycopg://...`
    to a sync-compatible psycopg URL for migrations.
    """
    url = make_url(settings.database_url)

    if url.drivername == "postgresql+psycopg":
        return str(url.set(drivername="postgresql+psycopg"))

    return settings.database_url


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
</file>

<file path="app/core/deps.py">
from __future__ import annotations

from dataclasses import dataclass

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.core.security import decode_access_token
from app.repositories.user_repository import UserRepository

bearer_scheme = HTTPBearer(auto_error=False)


@dataclass
class CurrentUser:
    id: str
    email: str
    business_id: str
    role: str
    is_active: bool


DbSessionDep = Depends(get_db_session)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db_session),
) -> CurrentUser:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials were not provided.",
        )

    token = credentials.credentials

    try:
        payload = decode_access_token(token)
    except InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token.",
        ) from exc

    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type.",
        )

    user_id = payload.get("sub")
    business_id = payload.get("business_id")
    role = payload.get("role")

    if not user_id or not business_id or not role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Malformed access token.",
        )

    user = await UserRepository(db).get_by_id(user_id)
    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is not active.",
        )

    return CurrentUser(
        id=user.id,
        email=user.email,
        business_id=business_id,
        role=role,
        is_active=user.is_active,
    )
</file>

<file path="app/core/logging.py">
import logging
import sys

import structlog

from app.core.config import get_settings


def configure_logging() -> None:
    settings = get_settings()
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)

    timestamper = structlog.processors.TimeStamper(fmt="iso", utc=True)

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_log_level,
            timestamper,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=log_level,
    )
</file>

<file path="app/core/security.py">
from __future__ import annotations

from datetime import UTC, datetime, timedelta
from secrets import token_urlsafe
from typing import Any

import jwt
from pwdlib import PasswordHash

from app.core.config import get_settings

settings = get_settings()
password_hasher = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return password_hasher.verify(password, password_hash)


def generate_session_token() -> str:
    return token_urlsafe(48)


def _build_token(
    *,
    subject: str,
    token_type: str,
    secret: str,
    expires_delta: timedelta,
    extra_claims: dict[str, Any] | None = None,
) -> str:
    now = datetime.now(UTC)
    payload: dict[str, Any] = {
        "sub": subject,
        "type": token_type,
        "iss": settings.jwt_issuer,
        "aud": settings.jwt_audience,
        "iat": int(now.timestamp()),
        "nbf": int(now.timestamp()),
        "exp": int((now + expires_delta).timestamp()),
    }

    if extra_claims:
        payload.update(extra_claims)

    return jwt.encode(payload, secret, algorithm="HS256")


def create_access_token(
    *,
    subject: str,
    business_id: str,
    role: str,
) -> str:
    return _build_token(
        subject=subject,
        token_type="access",
        secret=settings.jwt_access_token_secret,
        expires_delta=timedelta(minutes=settings.jwt_access_token_expires_minutes),
        extra_claims={
            "business_id": business_id,
            "role": role,
        },
    )


def create_refresh_token(
    *,
    subject: str,
    session_id: str,
) -> str:
    return _build_token(
        subject=subject,
        token_type="refresh",
        secret=settings.jwt_refresh_token_secret,
        expires_delta=timedelta(days=settings.jwt_refresh_token_expires_days),
        extra_claims={
            "session_id": session_id,
        },
    )


def decode_access_token(token: str) -> dict[str, Any]:
    return jwt.decode(
        token,
        settings.jwt_access_token_secret,
        algorithms=["HS256"],
        audience=settings.jwt_audience,
        issuer=settings.jwt_issuer,
    )


def decode_refresh_token(token: str) -> dict[str, Any]:
    return jwt.decode(
        token,
        settings.jwt_refresh_token_secret,
        algorithms=["HS256"],
        audience=settings.jwt_audience,
        issuer=settings.jwt_issuer,
    )


def get_refresh_token_expiry() -> datetime:
    return datetime.now(UTC) + timedelta(days=settings.jwt_refresh_token_expires_days)
</file>

<file path="app/core/tenancy.py">

</file>

<file path="app/main.py">
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.auth import router as auth_router
from app.api.routes.businesses import router as businesses_router
from app.api.routes.health import router as health_router
from app.api.routes.onboarding import router as onboarding_router
from app.api.routes.payment_providers import router as payment_providers_router
from app.api.routes.payments import router as payments_router
from app.api.routes.paystack_webhooks import router as paystack_webhooks_router
from app.api.routes.receipts import router as receipts_router
from app.api.routes.whatsapp_webhooks import router as whatsapp_webhooks_router
from app.core.config import get_settings
from app.core.logging import configure_logging

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    configure_logging()
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.app_debug,
    lifespan=lifespan,
)

if settings.cors_origins_list:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(businesses_router)
app.include_router(onboarding_router)
app.include_router(payment_providers_router)
app.include_router(payments_router)
app.include_router(receipts_router)
app.include_router(whatsapp_webhooks_router)
app.include_router(paystack_webhooks_router)


@app.get("/", summary="Root")
async def root() -> dict[str, str]:
    return {
        "message": "WapBiz backend is running.",
        "docs": "/docs",
    }
</file>

<file path="app/models/__init__.py">
from app.models.base import Base
from app.models.business import Business
from app.models.catalog_category import CatalogCategory
from app.models.catalog_item import CatalogItem
from app.models.conversation_session import ConversationSession
from app.models.customer import Customer
from app.models.message_log import MessageLog
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.payment import Payment
from app.models.payment_provider import PaymentProvider
from app.models.receipt import Receipt
from app.models.user import User
from app.models.user_session import UserSession
from app.models.webhook_event import WebhookEvent
from app.models.whatsapp_account import WhatsAppAccount

__all__ = [
    "Base",
    "Business",
    "CatalogCategory",
    "CatalogItem",
    "WhatsAppAccount",
    "Customer",
    "ConversationSession",
    "WebhookEvent",
    "MessageLog",
    "Order",
    "OrderItem",
    "PaymentProvider",
    "Payment",
    "Receipt",
    "User",
    "UserSession",
]
</file>

<file path="app/models/audit_log.py">

</file>

<file path="app/models/base.py">
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
</file>

<file path="app/models/business_settings.py">

</file>

<file path="app/models/business_user.py">

</file>

<file path="app/models/business.py">
from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Business(Base):
    __tablename__ = "businesses"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(255), index=True)
    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    status: Mapped[str] = mapped_column(String(50), default="active", index=True)
    plan: Mapped[str] = mapped_column(String(50), default="starter")
    country: Mapped[str | None] = mapped_column(String(100), nullable=True)
    currency: Mapped[str] = mapped_column(String(10), default="NGN")
    timezone: Mapped[str] = mapped_column(String(100), default="Africa/Lagos")
    contact_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    contact_phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    logo_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )
</file>

<file path="app/models/catalog_category.py">
from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class CatalogCategory(Base):
    __tablename__ = "catalog_categories"
    __table_args__ = (
        UniqueConstraint("business_id", "name", name="uq_catalog_categories_business_name"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id: Mapped[str] = mapped_column(String(36), ForeignKey("businesses.id"), index=True)
    name: Mapped[str] = mapped_column(String(120), index=True)
    slug: Mapped[str] = mapped_column(String(120), index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )
</file>

<file path="app/models/catalog_item.py">
from __future__ import annotations

import uuid
from datetime import UTC, datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class CatalogItem(Base):
    __tablename__ = "catalog_items"
    __table_args__ = (
        UniqueConstraint("business_id", "name", name="uq_catalog_items_business_name"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id: Mapped[str] = mapped_column(String(36), ForeignKey("businesses.id"), index=True)
    category_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("catalog_categories.id"),
        nullable=True,
        index=True,
    )
    external_catalog_id: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    currency: Mapped[str] = mapped_column(String(10), default="NGN")
    stock_status: Mapped[str] = mapped_column(String(50), default="in_stock", index=True)
    image_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )
</file>

<file path="app/models/conversation_session.py">
from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class ConversationSession(Base):
    __tablename__ = "conversation_sessions"
    __table_args__ = (
        UniqueConstraint("business_id", "customer_id", name="uq_sessions_business_customer"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id: Mapped[str] = mapped_column(String(36), ForeignKey("businesses.id"), index=True)
    customer_id: Mapped[str] = mapped_column(String(36), ForeignKey("customers.id"), index=True)
    current_state: Mapped[str] = mapped_column(String(100), default="idle", index=True)
    cart_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    context_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    last_incoming_message_id: Mapped[str | None] = mapped_column(String(150), nullable=True)
    last_outgoing_message_id: Mapped[str | None] = mapped_column(String(150), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    last_message_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )
</file>

<file path="app/models/customer.py">
from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Customer(Base):
    __tablename__ = "customers"
    __table_args__ = (
        UniqueConstraint("business_id", "whatsapp_number", name="uq_customers_business_number"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id: Mapped[str] = mapped_column(String(36), ForeignKey("businesses.id"), index=True)
    whatsapp_number: Mapped[str] = mapped_column(String(30), index=True)
    display_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    first_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    last_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
</file>

<file path="app/models/message_log.py">
from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class MessageLog(Base):
    __tablename__ = "message_logs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id: Mapped[str] = mapped_column(String(36), ForeignKey("businesses.id"), index=True)
    customer_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("customers.id"), nullable=True, index=True)
    conversation_session_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("conversation_sessions.id"),
        nullable=True,
        index=True,
    )
    direction: Mapped[str] = mapped_column(String(20), index=True)  # inbound | outbound
    channel: Mapped[str] = mapped_column(String(30), default="whatsapp", index=True)
    external_message_id: Mapped[str | None] = mapped_column(String(150), nullable=True, index=True)
    message_type: Mapped[str] = mapped_column(String(50), index=True)
    text_body: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    payload: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
</file>

<file path="app/models/order_item.py">
from __future__ import annotations

import uuid
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id: Mapped[str] = mapped_column(String(36), ForeignKey("orders.id"), index=True)
    catalog_item_id: Mapped[str] = mapped_column(String(36), ForeignKey("catalog_items.id"), index=True)
    quantity: Mapped[int] = mapped_column(default=1)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    line_total: Mapped[Decimal] = mapped_column(Numeric(12, 2))
</file>

<file path="app/models/order.py">
from __future__ import annotations

import uuid
from datetime import UTC, datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id: Mapped[str] = mapped_column(String(36), ForeignKey("businesses.id"), index=True)
    customer_id: Mapped[str] = mapped_column(String(36), ForeignKey("customers.id"), index=True)
    status: Mapped[str] = mapped_column(String(50), default="draft", index=True)
    subtotal: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0.00"))
    total: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0.00"))
    currency: Mapped[str] = mapped_column(String(10), default="NGN")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )
    paid_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
</file>

<file path="app/models/payment_provider.py">
from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class PaymentProvider(Base):
    __tablename__ = "payment_providers"
    __table_args__ = (
        UniqueConstraint("business_id", "provider", name="uq_payment_providers_business_provider"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id: Mapped[str] = mapped_column(String(36), ForeignKey("businesses.id"), index=True)
    provider: Mapped[str] = mapped_column(String(50), index=True)  # paystack, stripe later
    public_key_encrypted: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    secret_key_encrypted: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    webhook_secret_encrypted: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )
</file>

<file path="app/models/payment.py">
from __future__ import annotations

import uuid
from datetime import UTC, datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, JSON, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id: Mapped[str] = mapped_column(String(36), ForeignKey("businesses.id"), index=True)
    order_id: Mapped[str] = mapped_column(String(36), ForeignKey("orders.id"), index=True)
    provider: Mapped[str] = mapped_column(String(50), index=True)
    provider_reference: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    status: Mapped[str] = mapped_column(String(50), default="initialized", index=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    currency: Mapped[str] = mapped_column(String(10), default="NGN")
    authorization_url: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    access_code: Mapped[str | None] = mapped_column(String(255), nullable=True)
    raw_payload: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    paid_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )
</file>

<file path="app/models/receipt.py">
from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Receipt(Base):
    __tablename__ = "receipts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id: Mapped[str] = mapped_column(String(36), ForeignKey("businesses.id"), index=True)
    order_id: Mapped[str] = mapped_column(String(36), ForeignKey("orders.id"), index=True)
    payment_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("payments.id"), nullable=True, index=True)
    receipt_number: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    receipt_text: Mapped[str] = mapped_column(Text)
    customer_delivery_status: Mapped[str] = mapped_column(String(50), default="pending")
    owner_delivery_status: Mapped[str] = mapped_column(String(50), default="pending")
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
</file>

<file path="app/models/user_session.py">
from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class UserSession(Base):
    __tablename__ = "user_sessions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), index=True)
    business_id: Mapped[str] = mapped_column(String(36), ForeignKey("businesses.id"), index=True)
    refresh_token_hash: Mapped[str] = mapped_column(String(255))
    user_agent: Mapped[str | None] = mapped_column(Text, nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(64), nullable=True)
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    last_used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
</file>

<file path="app/models/user.py">
from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id: Mapped[str] = mapped_column(String(36), ForeignKey("businesses.id"), index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255))
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(50), default="owner")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )
</file>

<file path="app/models/webhook_event.py">
from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class WebhookEvent(Base):
    __tablename__ = "webhook_events"
    __table_args__ = (
        UniqueConstraint("source", "external_event_id", name="uq_webhook_source_external_event"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("businesses.id"),
        nullable=True,
        index=True,
    )
    source: Mapped[str] = mapped_column(String(50), index=True)
    external_event_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    payload: Mapped[dict] = mapped_column(JSON)
    signature: Mapped[str | None] = mapped_column(Text, nullable=True)
    processed: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    processed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
</file>

<file path="app/models/whatsapp_account.py">
from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class WhatsAppAccount(Base):
    __tablename__ = "whatsapp_accounts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id: Mapped[str] = mapped_column(String(36), ForeignKey("businesses.id"), index=True)
    phone_number_id: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    waba_id: Mapped[str] = mapped_column(String(100), index=True)
    business_phone: Mapped[str] = mapped_column(String(30), index=True)
    verify_token: Mapped[str] = mapped_column(String(255))
    access_token_encrypted: Mapped[str | None] = mapped_column(Text, nullable=True)
    app_secret_encrypted: Mapped[str | None] = mapped_column(Text, nullable=True)
    webhook_status: Mapped[str] = mapped_column(String(50), default="pending")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )
</file>

<file path="app/repositories/__init__.py">

</file>

<file path="app/repositories/audit_log_repository.py">

</file>

<file path="app/repositories/base.py">

</file>

<file path="app/repositories/business_repository.py">
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.business import Business
from app.models.whatsapp_account import WhatsAppAccount


class BusinessRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_id(self, business_id: str) -> Business | None:
        result = await self.db.execute(select(Business).where(Business.id == business_id))
        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Business | None:
        result = await self.db.execute(select(Business).where(Business.slug == slug))
        return result.scalar_one_or_none()

    async def get_by_phone_number_id(self, phone_number_id: str) -> Business | None:
        stmt = (
            select(Business)
            .join(WhatsAppAccount, WhatsAppAccount.business_id == Business.id)
            .where(WhatsAppAccount.phone_number_id == phone_number_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_business_and_whatsapp_account(
        self,
        phone_number_id: str,
    ) -> tuple[Business | None, WhatsAppAccount | None]:
        stmt = (
            select(Business, WhatsAppAccount)
            .join(WhatsAppAccount, WhatsAppAccount.business_id == Business.id)
            .where(WhatsAppAccount.phone_number_id == phone_number_id)
        )
        result = await self.db.execute(stmt)
        row = result.first()

        if row is None:
            return None, None

        return row[0], row[1]
</file>

<file path="app/repositories/business_settings_repository.py">

</file>

<file path="app/repositories/business_user_repository.py">

</file>

<file path="app/repositories/catalog_repository.py">
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.catalog_category import CatalogCategory
from app.models.catalog_item import CatalogItem


class CatalogRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_active_categories(self, business_id: str) -> list[CatalogCategory]:
        stmt = (
            select(CatalogCategory)
            .where(
                CatalogCategory.business_id == business_id,
                CatalogCategory.is_active.is_(True),
            )
            .order_by(CatalogCategory.name.asc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_active_items(self, business_id: str) -> list[CatalogItem]:
        stmt = (
            select(CatalogItem)
            .where(
                CatalogItem.business_id == business_id,
                CatalogItem.is_active.is_(True),
            )
            .order_by(CatalogItem.name.asc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_item_by_name(self, business_id: str, item_name: str) -> CatalogItem | None:
        stmt = select(CatalogItem).where(
            CatalogItem.business_id == business_id,
            CatalogItem.name.ilike(item_name),
            CatalogItem.is_active.is_(True),
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_item_by_id(self, business_id: str, item_id: str) -> CatalogItem | None:
        stmt = select(CatalogItem).where(
            CatalogItem.business_id == business_id,
            CatalogItem.id == item_id,
            CatalogItem.is_active.is_(True),
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
</file>

<file path="app/repositories/conversation_session_repository.py">
from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.conversation_session import ConversationSession


class ConversationSessionRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_business_and_customer(
        self,
        *,
        business_id: str,
        customer_id: str,
    ) -> ConversationSession | None:
        stmt = select(ConversationSession).where(
            ConversationSession.business_id == business_id,
            ConversationSession.customer_id == customer_id,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_or_create(
        self,
        *,
        business_id: str,
        customer_id: str,
    ) -> ConversationSession:
        session = await self.get_by_business_and_customer(
            business_id=business_id,
            customer_id=customer_id,
        )
        if session:
            session.last_message_at = datetime.now(UTC)
            await self.db.flush()
            return session

        session = ConversationSession(
            business_id=business_id,
            customer_id=customer_id,
        )
        self.db.add(session)
        await self.db.flush()
        return session

    async def update_state(
        self,
        *,
        session: ConversationSession,
        current_state: str,
        context_json: dict | None = None,
        cart_json: dict | None = None,
        last_incoming_message_id: str | None = None,
        last_outgoing_message_id: str | None = None,
    ) -> ConversationSession:
        session.current_state = current_state
        session.last_message_at = datetime.now(UTC)

        if context_json is not None:
            session.context_json = context_json
        if cart_json is not None:
            session.cart_json = cart_json
        if last_incoming_message_id is not None:
            session.last_incoming_message_id = last_incoming_message_id
        if last_outgoing_message_id is not None:
            session.last_outgoing_message_id = last_outgoing_message_id

        await self.db.flush()
        return session
</file>

<file path="app/repositories/customer_repository.py">
from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.customer import Customer


class CustomerRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_business_and_number(self, business_id: str, whatsapp_number: str) -> Customer | None:
        stmt = select(Customer).where(
            Customer.business_id == business_id,
            Customer.whatsapp_number == whatsapp_number,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_or_create(
        self,
        *,
        business_id: str,
        whatsapp_number: str,
        display_name: str | None,
    ) -> Customer:
        customer = await self.get_by_business_and_number(business_id, whatsapp_number)
        if customer:
            customer.display_name = display_name or customer.display_name
            customer.last_seen_at = datetime.now(UTC)
            await self.db.flush()
            return customer

        customer = Customer(
            business_id=business_id,
            whatsapp_number=whatsapp_number,
            display_name=display_name,
        )
        self.db.add(customer)
        await self.db.flush()
        return customer
</file>

<file path="app/repositories/message_log_repository.py">
from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.message_log import MessageLog


class MessageLogRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(
        self,
        *,
        business_id: str,
        customer_id: str | None,
        conversation_session_id: str | None,
        direction: str,
        message_type: str,
        text_body: str | None = None,
        external_message_id: str | None = None,
        status: str | None = None,
        payload: dict | None = None,
    ) -> MessageLog:
        message_log = MessageLog(
            business_id=business_id,
            customer_id=customer_id,
            conversation_session_id=conversation_session_id,
            direction=direction,
            message_type=message_type,
            text_body=text_body,
            external_message_id=external_message_id,
            status=status,
            payload=payload,
        )
        self.db.add(message_log)
        await self.db.flush()
        return message_log
</file>

<file path="app/repositories/order_repository.py">
from __future__ import annotations

from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import Order
from app.models.order_item import OrderItem


class OrderRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_active_draft_by_customer(self, business_id: str, customer_id: str) -> Order | None:
        stmt = select(Order).where(
            Order.business_id == business_id,
            Order.customer_id == customer_id,
            Order.status == "draft",
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id(self, order_id: str) -> Order | None:
        stmt = select(Order).where(Order.id == order_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_draft(
        self,
        *,
        business_id: str,
        customer_id: str,
        currency: str,
    ) -> Order:
        order = Order(
            business_id=business_id,
            customer_id=customer_id,
            currency=currency,
            status="draft",
            subtotal=Decimal("0.00"),
            total=Decimal("0.00"),
        )
        self.db.add(order)
        await self.db.flush()
        return order

    async def add_item(
        self,
        *,
        order_id: str,
        catalog_item_id: str,
        quantity: int,
        unit_price: Decimal,
    ) -> OrderItem:
        line_total = unit_price * quantity
        item = OrderItem(
            order_id=order_id,
            catalog_item_id=catalog_item_id,
            quantity=quantity,
            unit_price=unit_price,
            line_total=line_total,
        )
        self.db.add(item)
        await self.db.flush()
        return item

    async def recalculate_totals(self, order: Order) -> Order:
        stmt = select(OrderItem).where(OrderItem.order_id == order.id)
        result = await self.db.execute(stmt)
        items = list(result.scalars().all())

        subtotal = sum((item.line_total for item in items), Decimal("0.00"))
        order.subtotal = subtotal
        order.total = subtotal
        await self.db.flush()
        return order

    async def mark_pending_payment(self, order: Order) -> Order:
        order.status = "pending_payment"
        await self.db.flush()
        return order
</file>

<file path="app/repositories/payment_provider_repository.py">
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.payment_provider import PaymentProvider


class PaymentProviderRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_active_by_business_and_provider(
        self,
        *,
        business_id: str,
        provider: str,
    ) -> PaymentProvider | None:
        stmt = select(PaymentProvider).where(
            PaymentProvider.business_id == business_id,
            PaymentProvider.provider == provider,
            PaymentProvider.is_active.is_(True),
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(
        self,
        *,
        business_id: str,
        provider: str,
        public_key_encrypted: str | None,
        secret_key_encrypted: str,
        webhook_secret_encrypted: str | None,
    ) -> PaymentProvider:
        payment_provider = PaymentProvider(
            business_id=business_id,
            provider=provider,
            public_key_encrypted=public_key_encrypted,
            secret_key_encrypted=secret_key_encrypted,
            webhook_secret_encrypted=webhook_secret_encrypted,
            is_active=True,
        )
        self.db.add(payment_provider)
        await self.db.flush()
        return payment_provider
</file>

<file path="app/repositories/payment_repository.py">
from __future__ import annotations

from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.payment import Payment


class PaymentRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_reference(self, provider_reference: str) -> Payment | None:
        stmt = select(Payment).where(Payment.provider_reference == provider_reference)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(
        self,
        *,
        business_id: str,
        order_id: str,
        provider: str,
        provider_reference: str,
        amount: Decimal,
        currency: str,
        authorization_url: str | None = None,
        access_code: str | None = None,
        raw_payload: dict | None = None,
    ) -> Payment:
        payment = Payment(
            business_id=business_id,
            order_id=order_id,
            provider=provider,
            provider_reference=provider_reference,
            amount=amount,
            currency=currency,
            authorization_url=authorization_url,
            access_code=access_code,
            raw_payload=raw_payload,
            status="initialized",
        )
        self.db.add(payment)
        await self.db.flush()
        return payment
</file>

<file path="app/repositories/receipt_repository.py">
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.receipt import Receipt


class ReceiptRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_order_id(self, order_id: str) -> Receipt | None:
        stmt = select(Receipt).where(Receipt.order_id == order_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(
        self,
        *,
        business_id: str,
        order_id: str,
        payment_id: str | None,
        receipt_number: str,
        receipt_text: str,
    ) -> Receipt:
        receipt = Receipt(
            business_id=business_id,
            order_id=order_id,
            payment_id=payment_id,
            receipt_number=receipt_number,
            receipt_text=receipt_text,
        )
        self.db.add(receipt)
        await self.db.flush()
        return receipt
</file>

<file path="app/repositories/setup_repository.py">
from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.business import Business
from app.models.user import User
from app.models.whatsapp_account import WhatsAppAccount


class SetupRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_business(
        self,
        *,
        name: str,
        slug: str,
        contact_email: str | None,
        contact_phone: str | None,
        country: str | None,
        currency: str,
        timezone: str,
    ) -> Business:
        business = Business(
            name=name,
            slug=slug,
            contact_email=contact_email,
            contact_phone=contact_phone,
            country=country,
            currency=currency,
            timezone=timezone,
        )
        self.db.add(business)
        await self.db.flush()
        return business

    async def create_owner_user(
        self,
        *,
        business_id: str,
        full_name: str,
        email: str,
        password_hash: str,
    ) -> User:
        user = User(
            business_id=business_id,
            full_name=full_name,
            email=email,
            password_hash=password_hash,
            role="owner",
            is_active=True,
        )
        self.db.add(user)
        await self.db.flush()
        return user

    async def create_whatsapp_account(
        self,
        *,
        business_id: str,
        phone_number_id: str,
        waba_id: str,
        business_phone: str,
        verify_token: str,
        access_token_encrypted: str,
        app_secret_encrypted: str | None,
    ) -> WhatsAppAccount:
        whatsapp_account = WhatsAppAccount(
            business_id=business_id,
            phone_number_id=phone_number_id,
            waba_id=waba_id,
            business_phone=business_phone,
            verify_token=verify_token,
            access_token_encrypted=access_token_encrypted,
            app_secret_encrypted=app_secret_encrypted,
            webhook_status="pending",
            is_active=True,
        )
        self.db.add(whatsapp_account)
        await self.db.flush()
        return whatsapp_account
</file>

<file path="app/repositories/user_repository.py">
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_id(self, user_id: str) -> User | None:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create(
        self,
        *,
        business_id: str,
        email: str,
        full_name: str,
        password_hash: str,
        role: str,
    ) -> User:
        user = User(
            business_id=business_id,
            email=email,
            full_name=full_name,
            password_hash=password_hash,
            role=role,
        )
        self.db.add(user)
        await self.db.flush()
        return user
</file>

<file path="app/repositories/user_session_repository.py">
from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_session import UserSession


class UserSessionRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_id(self, session_id: str) -> UserSession | None:
        result = await self.db.execute(select(UserSession).where(UserSession.id == session_id))
        return result.scalar_one_or_none()

    async def create(
        self,
        *,
        user_id: str,
        business_id: str,
        refresh_token_hash: str,
        expires_at: datetime,
        user_agent: str | None = None,
        ip_address: str | None = None,
    ) -> UserSession:
        session = UserSession(
            user_id=user_id,
            business_id=business_id,
            refresh_token_hash=refresh_token_hash,
            expires_at=expires_at,
            user_agent=user_agent,
            ip_address=ip_address,
        )
        self.db.add(session)
        await self.db.flush()
        return session

    async def revoke(self, session: UserSession) -> None:
        session.is_revoked = True
        session.revoked_at = datetime.now(UTC)
        await self.db.flush()

    async def touch(self, session: UserSession) -> None:
        session.last_used_at = datetime.now(UTC)
        await self.db.flush()
</file>

<file path="app/repositories/webhook_event_repository.py">
from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.webhook_event import WebhookEvent


class WebhookEventRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_source_and_external_event_id(
        self,
        *,
        source: str,
        external_event_id: str,
    ) -> WebhookEvent | None:
        stmt = select(WebhookEvent).where(
            WebhookEvent.source == source,
            WebhookEvent.external_event_id == external_event_id,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(
        self,
        *,
        business_id: str | None,
        source: str,
        external_event_id: str | None,
        payload: dict,
        signature: str | None = None,
    ) -> WebhookEvent:
        event = WebhookEvent(
            business_id=business_id,
            source=source,
            external_event_id=external_event_id,
            payload=payload,
            signature=signature,
        )
        self.db.add(event)
        await self.db.flush()
        return event

    async def mark_processed(self, event: WebhookEvent) -> None:
        event.processed = True
        event.processed_at = datetime.now(UTC)
        await self.db.flush()
</file>

<file path="app/repositories/whatsapp_account_repository.py">
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.whatsapp_account import WhatsAppAccount


class WhatsAppAccountRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_phone_number_id(self, phone_number_id: str) -> WhatsAppAccount | None:
        stmt = select(WhatsAppAccount).where(WhatsAppAccount.phone_number_id == phone_number_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_verify_token(self, verify_token: str) -> WhatsAppAccount | None:
        stmt = select(WhatsAppAccount).where(WhatsAppAccount.verify_token == verify_token)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
</file>

<file path="app/schemas/__init__.py">

</file>

<file path="app/schemas/auth.py">
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
</file>

<file path="app/schemas/business_settings.py">

</file>

<file path="app/schemas/business_user.py">

</file>

<file path="app/schemas/business.py">
from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field, field_validator


class CreateBusinessRequest(BaseModel):
    business_name: str = Field(min_length=2, max_length=255)
    business_slug: str = Field(min_length=2, max_length=120)
    contact_email: EmailStr | None = None
    contact_phone: str | None = Field(default=None, max_length=30)
    country: str | None = Field(default=None, max_length=100)
    currency: str = Field(default="NGN", max_length=10)
    timezone: str = Field(default="Africa/Lagos", max_length=100)

    owner_full_name: str = Field(min_length=2, max_length=255)
    owner_email: EmailStr
    owner_password: str = Field(min_length=8, max_length=128)

    whatsapp_phone_number_id: str = Field(min_length=2, max_length=100)
    whatsapp_waba_id: str = Field(min_length=2, max_length=100)
    whatsapp_business_phone: str = Field(min_length=5, max_length=30)
    whatsapp_verify_token: str = Field(min_length=6, max_length=255)
    whatsapp_access_token: str = Field(min_length=10)
    whatsapp_app_secret: str | None = Field(default=None, min_length=10)

    @field_validator("business_slug", mode="before")
    @classmethod
    def normalize_business_slug(cls, value: object) -> object:
        if isinstance(value, str):
            return value.strip().lower().replace(" ", "-")
        return value

    @field_validator(
        "business_name",
        "owner_full_name",
        "whatsapp_business_phone",
        "whatsapp_phone_number_id",
        "whatsapp_waba_id",
        "whatsapp_verify_token",
        mode="before",
    )
    @classmethod
    def strip_string_fields(cls, value: object) -> object:
        if isinstance(value, str):
            return value.strip()
        return value


class CreateBusinessResponse(BaseModel):
    business_id: str
    business_name: str
    owner_user_id: str
    whatsapp_account_id: str
    message: str
</file>

<file path="app/schemas/catalog.py">
from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel


class CatalogItemSummary(BaseModel):
    id: str
    name: str
    description: str | None
    price: Decimal
    currency: str


class CatalogBrowseResult(BaseModel):
    business_id: str
    items: list[CatalogItemSummary]
    message: str
</file>

<file path="app/schemas/common.py">
from __future__ import annotations

from pydantic import BaseModel


class MessageResponse(BaseModel):
    message: str


class HealthResponse(BaseModel):
    status: str
    service: str
    environment: str
    version: str
</file>

<file path="app/schemas/customer.py">

</file>

<file path="app/schemas/metrics.py">

</file>

<file path="app/schemas/order.py">

</file>

<file path="app/schemas/outbound_whatsapp.py">
from __future__ import annotations

from pydantic import BaseModel


class OutboundWhatsAppTextMessage(BaseModel):
    business_id: str
    to: str
    body: str
</file>

<file path="app/schemas/payment_provider.py">
from __future__ import annotations

from pydantic import BaseModel, Field


class CreatePaymentProviderRequest(BaseModel):
    business_id: str
    provider: str = Field(default="paystack", max_length=50)
    public_key: str | None = None
    secret_key: str
    webhook_secret: str | None = None


class CreatePaymentProviderResponse(BaseModel):
    payment_provider_id: str
    business_id: str
    provider: str
    message: str
</file>

<file path="app/schemas/payment.py">
from __future__ import annotations

from pydantic import BaseModel, EmailStr


class InitializePaymentRequest(BaseModel):
    order_id: str
    customer_email: EmailStr


class InitializePaymentResponse(BaseModel):
    order_id: str
    payment_reference: str
    authorization_url: str
    access_code: str | None = None
    status: str
</file>

<file path="app/schemas/paystack.py">

</file>

<file path="app/schemas/receipt.py">
from __future__ import annotations

from pydantic import BaseModel


class ReceiptResponse(BaseModel):
    receipt_id: str
    receipt_number: str
    order_id: str
    receipt_text: str
</file>

<file path="app/schemas/whatsapp.py">
from __future__ import annotations

from pydantic import BaseModel


class IncomingWhatsAppMessage(BaseModel):
    business_id: str
    phone_number_id: str
    customer_number: str
    customer_name: str | None = None
    message_id: str
    message_type: str
    text_body: str | None = None
    raw_payload: dict
</file>

<file path="app/services/__init__.py">

</file>

<file path="app/services/audit_service.py">

</file>

<file path="app/services/auth_service.py">
from __future__ import annotations

from datetime import UTC, datetime

from fastapi import HTTPException, status
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    get_refresh_token_expiry,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.repositories.user_session_repository import UserSessionRepository


class AuthService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.user_repo = UserRepository(db)
        self.session_repo = UserSessionRepository(db)

    async def authenticate_user(self, *, email: str, password: str) -> User:
        user = await self.user_repo.get_by_email(email)
        if user is None or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        if not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        return user

    async def login(
        self,
        *,
        email: str,
        password: str,
        user_agent: str | None = None,
        ip_address: str | None = None,
    ) -> dict[str, str]:
        user = await self.authenticate_user(email=email, password=password)

        placeholder_refresh_value = hash_password(f"{user.id}:{datetime.now(UTC).timestamp()}")
        session = await self.session_repo.create(
            user_id=user.id,
            business_id=user.business_id,
            refresh_token_hash=placeholder_refresh_value,
            expires_at=get_refresh_token_expiry(),
            user_agent=user_agent,
            ip_address=ip_address,
        )

        refresh_token = create_refresh_token(subject=user.id, session_id=session.id)
        session.refresh_token_hash = hash_password(refresh_token)
        await self.db.flush()

        access_token = create_access_token(
            subject=user.id,
            business_id=user.business_id,
            role=user.role,
        )

        await self.db.commit()

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    async def refresh_tokens(self, *, refresh_token: str) -> dict[str, str]:
        try:
            payload = decode_refresh_token(refresh_token)
        except InvalidTokenError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token.",
            ) from exc

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type.",
            )

        user_id = payload.get("sub")
        session_id = payload.get("session_id")
        if not user_id or not session_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Malformed refresh token.",
            )

        session = await self.session_repo.get_by_id(session_id)
        if session is None or session.is_revoked:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session is invalid or revoked.",
            )

        if session.expires_at <= datetime.now(UTC):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session has expired.",
            )

        if not verify_password(refresh_token, session.refresh_token_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token mismatch.",
            )

        user = await self.user_repo.get_by_id(user_id)
        if user is None or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User account is not active.",
            )

        new_refresh_token = create_refresh_token(subject=user.id, session_id=session.id)
        session.refresh_token_hash = hash_password(new_refresh_token)
        await self.session_repo.touch(session)

        new_access_token = create_access_token(
            subject=user.id,
            business_id=user.business_id,
            role=user.role,
        )

        await self.db.commit()

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
        }
</file>

<file path="app/services/catalog_service.py">
from __future__ import annotations

from app.repositories.catalog_repository import CatalogRepository
from app.schemas.catalog import CatalogBrowseResult, CatalogItemSummary


class CatalogService:
    def __init__(self, catalog_repo: CatalogRepository) -> None:
        self.catalog_repo = catalog_repo

    async def build_catalog_browse_result(self, business_id: str) -> CatalogBrowseResult:
        items = await self.catalog_repo.get_active_items(business_id)

        if not items:
            return CatalogBrowseResult(
                business_id=business_id,
                items=[],
                message="Our catalog is currently empty. Please check back later or type *help*.",
            )

        summaries = [
            CatalogItemSummary(
                id=item.id,
                name=item.name,
                description=item.description,
                price=item.price,
                currency=item.currency,
            )
            for item in items[:10]
        ]

        lines = ["🛍️ Available products:"]
        for index, item in enumerate(summaries, start=1):
            lines.append(f"{index}. {item.name} — {item.currency} {item.price}")

        lines.append("")
        lines.append("Reply with the product name to start an order.")

        return CatalogBrowseResult(
            business_id=business_id,
            items=summaries,
            message="\n".join(lines),
        )
</file>

<file path="app/services/conversation_service.py">
from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.catalog_repository import CatalogRepository
from app.repositories.conversation_session_repository import ConversationSessionRepository
from app.repositories.customer_repository import CustomerRepository
from app.repositories.message_log_repository import MessageLogRepository
from app.schemas.whatsapp import IncomingWhatsAppMessage
from app.services.catalog_service import CatalogService
from app.services.order_service import OrderService
from app.services.whatsapp_reply_service import WhatsAppReplyService


class ConversationService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.customer_repo = CustomerRepository(db)
        self.session_repo = ConversationSessionRepository(db)
        self.message_log_repo = MessageLogRepository(db)
        self.catalog_service = CatalogService(CatalogRepository(db))
        self.order_service = OrderService(db)
        self.reply_service = WhatsAppReplyService()

    async def handle_incoming_message(self, message: IncomingWhatsAppMessage) -> dict:
        customer = await self.customer_repo.get_or_create(
            business_id=message.business_id,
            whatsapp_number=message.customer_number,
            display_name=message.customer_name,
        )

        session = await self.session_repo.get_or_create(
            business_id=message.business_id,
            customer_id=customer.id,
        )

        await self.message_log_repo.create(
            business_id=message.business_id,
            customer_id=customer.id,
            conversation_session_id=session.id,
            direction="inbound",
            message_type=message.message_type,
            text_body=message.text_body,
            external_message_id=message.message_id,
            payload=message.raw_payload,
        )

        next_state = session.current_state
        context_json = session.context_json or {}
        reply_text = self.reply_service.build_text_reply(state=next_state)

        if message.message_type == "text" and message.text_body:
            normalized_text = message.text_body.strip()
            lowered_text = normalized_text.lower()

            if lowered_text in {"hi", "hello", "hey", "start"}:
                next_state = "greeting"
                reply_text = self.reply_service.build_text_reply(state=next_state)

            elif lowered_text in {"menu", "catalog", "products"}:
                next_state = "catalog_browsing"
                catalog_result = await self.catalog_service.build_catalog_browse_result(
                    message.business_id
                )
                reply_text = catalog_result.message

            elif lowered_text in {"help", "human"}:
                next_state = "human_handoff_requested"
                reply_text = self.reply_service.build_text_reply(state=next_state)

            else:
                try:
                    draft_result = await self.order_service.create_or_update_draft_order_from_item_name(
                        business_id=message.business_id,
                        customer_id=customer.id,
                        item_name=normalized_text,
                        quantity=1,
                    )
                    next_state = "order_draft_created"
                    reply_text = (
                        f"✅ Added *{draft_result['item_name']}* to your draft order.\n\n"
                        f"Quantity: {draft_result['quantity']}\n"
                        f"Subtotal: {draft_result['currency']} {draft_result['subtotal']}\n\n"
                        "Reply with another product name to add more, or type *checkout* to continue."
                    )
                    context_json = {
                        **context_json,
                        "active_order_id": draft_result["order_id"],
                    }
                except HTTPException as exc:
                    if exc.status_code == 404:
                        reply_text = (
                            "I didn't understand that selection.\n\n"
                            "Type *menu* to view available products, or type *help* for assistance."
                        )
                    else:
                        raise

            context_json = {
                **context_json,
                "last_user_text": message.text_body,
            }

        await self.session_repo.update_state(
            session=session,
            current_state=next_state,
            context_json=context_json,
            last_incoming_message_id=message.message_id,
        )

        await self.db.flush()

        return {
            "business_id": message.business_id,
            "customer_id": customer.id,
            "session_id": session.id,
            "current_state": next_state,
            "message_type": message.message_type,
            "text_body": message.text_body,
            "reply_text": reply_text,
            "customer_number": message.customer_number,
            "phone_number_id": message.phone_number_id,
        }
</file>

<file path="app/services/customer_service.py">

</file>

<file path="app/services/metrics_service.py">

</file>

<file path="app/services/notification_service.py">

</file>

<file path="app/services/onboarding_service.py">

</file>

<file path="app/services/order_service.py">
from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.catalog_repository import CatalogRepository
from app.repositories.order_repository import OrderRepository


class OrderService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.catalog_repo = CatalogRepository(db)
        self.order_repo = OrderRepository(db)

    async def create_or_update_draft_order_from_item_name(
        self,
        *,
        business_id: str,
        customer_id: str,
        item_name: str,
        quantity: int = 1,
    ) -> dict:
        catalog_item = await self.catalog_repo.get_item_by_name(business_id, item_name)
        if catalog_item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Catalog item not found.",
            )

        order = await self.order_repo.get_active_draft_by_customer(business_id, customer_id)
        if order is None:
            order = await self.order_repo.create_draft(
                business_id=business_id,
                customer_id=customer_id,
                currency=catalog_item.currency,
            )

        await self.order_repo.add_item(
            order_id=order.id,
            catalog_item_id=catalog_item.id,
            quantity=quantity,
            unit_price=catalog_item.price,
        )
        order = await self.order_repo.recalculate_totals(order)

        await self.db.flush()

        return {
            "order_id": order.id,
            "status": order.status,
            "currency": order.currency,
            "subtotal": str(order.subtotal),
            "item_name": catalog_item.name,
            "quantity": quantity,
        }
</file>

<file path="app/services/payment_provider_service.py">
from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.business_repository import BusinessRepository
from app.repositories.payment_provider_repository import PaymentProviderRepository
from app.schemas.payment_provider import CreatePaymentProviderRequest
from app.utils.encryption import encrypt_value


class PaymentProviderService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.business_repo = BusinessRepository(db)
        self.provider_repo = PaymentProviderRepository(db)

    async def create_payment_provider(
        self,
        payload: CreatePaymentProviderRequest,
    ) -> dict:
        business = await self.business_repo.get_by_id(payload.business_id)
        if business is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Business not found.",
            )

        existing = await self.provider_repo.get_active_by_business_and_provider(
            business_id=payload.business_id,
            provider=payload.provider,
        )
        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Active payment provider already exists for this business.",
            )

        provider = await self.provider_repo.create(
            business_id=payload.business_id,
            provider=payload.provider,
            public_key_encrypted=encrypt_value(payload.public_key) if payload.public_key else None,
            secret_key_encrypted=encrypt_value(payload.secret_key),
            webhook_secret_encrypted=encrypt_value(payload.webhook_secret)
            if payload.webhook_secret
            else None,
        )
        await self.db.commit()

        return {
            "payment_provider_id": provider.id,
            "business_id": provider.business_id,
            "provider": provider.provider,
            "message": "Payment provider created successfully.",
        }
</file>

<file path="app/services/payment_service.py">
from __future__ import annotations

import uuid
from decimal import Decimal, ROUND_HALF_UP

import httpx
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.order_repository import OrderRepository
from app.repositories.payment_provider_repository import PaymentProviderRepository
from app.repositories.payment_repository import PaymentRepository
from app.schemas.payment import InitializePaymentRequest
from app.utils.encryption import decrypt_value


class PaymentService:
    PAYSTACK_INITIALIZE_URL = "https://api.paystack.co/transaction/initialize"

    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.order_repo = OrderRepository(db)
        self.provider_repo = PaymentProviderRepository(db)
        self.payment_repo = PaymentRepository(db)

    async def initialize_paystack_payment(
        self,
        payload: InitializePaymentRequest,
    ) -> dict:
        order = await self.order_repo.get_by_id(payload.order_id)
        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found.",
            )

        if order.total <= Decimal("0.00"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Order total must be greater than zero before payment initialization.",
            )

        provider = await self.provider_repo.get_active_by_business_and_provider(
            business_id=order.business_id,
            provider="paystack",
        )
        if provider is None or not provider.secret_key_encrypted:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Active Paystack configuration not found for this business.",
            )

        secret_key = decrypt_value(provider.secret_key_encrypted)
        reference = f"wapbiz-{order.id}-{uuid.uuid4().hex[:10]}"

        normalized_total = order.total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        amount_kobo = int(normalized_total * 100)

        request_payload = {
            "email": payload.customer_email,
            "amount": amount_kobo,
            "reference": reference,
            "currency": order.currency,
            "metadata": {
                "business_id": order.business_id,
                "order_id": order.id,
            },
        }

        headers = {
            "Authorization": f"Bearer {secret_key}",
            "Content-Type": "application/json",
        }

        try:
            async with httpx.AsyncClient(timeout=20.0) as client:
                response = await client.post(
                    self.PAYSTACK_INITIALIZE_URL,
                    headers=headers,
                    json=request_payload,
                )
                response.raise_for_status()
                provider_response = response.json()
        except httpx.HTTPError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Unable to initialize Paystack payment at this time.",
            ) from exc

        data = provider_response.get("data") or {}
        authorization_url = data.get("authorization_url")
        access_code = data.get("access_code")

        if not authorization_url:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Payment provider did not return an authorization URL.",
            )

        await self.payment_repo.create(
            business_id=order.business_id,
            order_id=order.id,
            provider="paystack",
            provider_reference=reference,
            amount=order.total,
            currency=order.currency,
            authorization_url=authorization_url,
            access_code=access_code,
            raw_payload=provider_response,
        )
        await self.order_repo.mark_pending_payment(order)
        await self.db.commit()

        return {
            "order_id": order.id,
            "payment_reference": reference,
            "authorization_url": authorization_url,
            "access_code": access_code,
            "status": "initialized",
        }
</file>

<file path="app/services/receipt_service.py">
from __future__ import annotations

import uuid
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.business import Business
from app.models.customer import Customer
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.payment import Payment
from app.models.catalog_item import CatalogItem
from app.repositories.receipt_repository import ReceiptRepository


class ReceiptService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.receipt_repo = ReceiptRepository(db)

    async def generate_receipt_for_order(self, order_id: str) -> dict:
        existing = await self.receipt_repo.get_by_order_id(order_id)
        if existing is not None:
            return {
                "receipt_id": existing.id,
                "receipt_number": existing.receipt_number,
                "order_id": existing.order_id,
                "receipt_text": existing.receipt_text,
            }

        order = await self.db.scalar(select(Order).where(Order.id == order_id))
        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found.",
            )

        business = await self.db.scalar(select(Business).where(Business.id == order.business_id))
        customer = await self.db.scalar(select(Customer).where(Customer.id == order.customer_id))
        payment = await self.db.scalar(
            select(Payment).where(Payment.order_id == order.id).order_by(Payment.created_at.desc())
        )

        order_items_result = await self.db.execute(
            select(OrderItem, CatalogItem)
            .join(CatalogItem, CatalogItem.id == OrderItem.catalog_item_id)
            .where(OrderItem.order_id == order.id)
        )
        order_items = order_items_result.all()

        if business is None or customer is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Order relationships are incomplete.",
            )

        receipt_number = f"RCPT-{uuid.uuid4().hex[:12].upper()}"

        lines = [
            f"Receipt Number: {receipt_number}",
            f"Business: {business.name}",
            f"Order ID: {order.id}",
            f"Customer: {customer.display_name or customer.whatsapp_number}",
            f"Currency: {order.currency}",
            "",
            "Items:",
        ]

        subtotal = Decimal("0.00")
        for order_item, catalog_item in order_items:
            lines.append(
                f"- {catalog_item.name} x {order_item.quantity} = {order.currency} {order_item.line_total}"
            )
            subtotal += order_item.line_total

        lines.extend(
            [
                "",
                f"Subtotal: {order.currency} {subtotal}",
                f"Total: {order.currency} {order.total}",
                f"Payment Status: {payment.status if payment else 'pending'}",
                f"Payment Reference: {payment.provider_reference if payment else 'N/A'}",
            ]
        )

        receipt_text = "\n".join(lines)

        receipt = await self.receipt_repo.create(
            business_id=order.business_id,
            order_id=order.id,
            payment_id=payment.id if payment else None,
            receipt_number=receipt_number,
            receipt_text=receipt_text,
        )
        await self.db.commit()

        return {
            "receipt_id": receipt.id,
            "receipt_number": receipt.receipt_number,
            "order_id": receipt.order_id,
            "receipt_text": receipt.receipt_text,
        }
</file>

<file path="app/services/setup_service.py">
from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.models.business import Business
from app.models.user import User
from app.models.whatsapp_account import WhatsAppAccount
from app.repositories.setup_repository import SetupRepository
from app.schemas.business import CreateBusinessRequest
from app.utils.encryption import encrypt_value


class SetupService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.repo = SetupRepository(db)

    async def create_business_with_owner_and_whatsapp(
        self,
        payload: CreateBusinessRequest,
    ) -> tuple[Business, User, WhatsAppAccount]:
        normalized_slug = payload.business_slug.strip().lower()
        normalized_owner_email = payload.owner_email.strip().lower()

        existing_business = await self.db.scalar(
            select(Business).where(Business.slug == normalized_slug)
        )
        if existing_business is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Business slug already exists.",
            )

        existing_user = await self.db.scalar(
            select(User).where(User.email == normalized_owner_email)
        )
        if existing_user is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Owner email already exists.",
            )

        existing_whatsapp = await self.db.scalar(
            select(WhatsAppAccount).where(
                WhatsAppAccount.phone_number_id == payload.whatsapp_phone_number_id
            )
        )
        if existing_whatsapp is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="WhatsApp phone number ID already exists.",
            )

        business = await self.repo.create_business(
            name=payload.business_name.strip(),
            slug=normalized_slug,
            contact_email=payload.contact_email,
            contact_phone=payload.contact_phone,
            country=payload.country,
            currency=payload.currency.upper(),
            timezone=payload.timezone,
        )

        owner = await self.repo.create_owner_user(
            business_id=business.id,
            full_name=payload.owner_full_name.strip(),
            email=normalized_owner_email,
            password_hash=hash_password(payload.owner_password),
        )

        whatsapp_account = await self.repo.create_whatsapp_account(
            business_id=business.id,
            phone_number_id=payload.whatsapp_phone_number_id,
            waba_id=payload.whatsapp_waba_id,
            business_phone=payload.whatsapp_business_phone,
            verify_token=payload.whatsapp_verify_token,
            access_token_encrypted=encrypt_value(payload.whatsapp_access_token),
            app_secret_encrypted=encrypt_value(payload.whatsapp_app_secret)
            if payload.whatsapp_app_secret
            else None,
        )

        await self.db.commit()
        return business, owner, whatsapp_account
</file>

<file path="app/services/tenant_service.py">

</file>

<file path="app/services/webhook_security_service.py">
from __future__ import annotations

import hashlib
import hmac

from app.utils.encryption import decrypt_value


class WebhookSecurityService:
    @staticmethod
    def verify_meta_signature(
        *,
        raw_body: bytes,
        signature_header: str | None,
        app_secret_encrypted: str | None,
    ) -> bool:
        if not signature_header or not app_secret_encrypted:
            return False

        expected_prefix = "sha256="
        if not signature_header.startswith(expected_prefix):
            return False

        app_secret = decrypt_value(app_secret_encrypted)
        expected_signature = hmac.new(
            key=app_secret.encode(),
            msg=raw_body,
            digestmod=hashlib.sha256,
        ).hexdigest()

        received_signature = signature_header[len(expected_prefix):]
        return hmac.compare_digest(expected_signature, received_signature)

    @staticmethod
    def verify_paystack_signature(
        *,
        raw_body: bytes,
        signature_header: str | None,
        secret_key: str | None,
    ) -> bool:
        if not signature_header or not secret_key:
            return False

        expected_signature = hmac.new(
            key=secret_key.encode(),
            msg=raw_body,
            digestmod=hashlib.sha512,
        ).hexdigest()

        return hmac.compare_digest(expected_signature, signature_header)
</file>

<file path="app/services/whatsapp_reply_service.py">
from __future__ import annotations


class WhatsAppReplyService:
    def build_text_reply(self, *, state: str, business_name: str | None = None) -> str:
        display_name = business_name or "WapBiz"

        if state == "greeting":
            return (
                f"👋 Welcome to {display_name}.\n\n"
                "Type *menu* to browse our catalog, or type *help* to request human assistance."
            )

        if state == "catalog_browsing":
            return "🛍️ Loading our catalog for you..."

        if state == "human_handoff_requested":
            return (
                "🤝 A human support request has been noted.\n\n"
                "Someone from the business team will follow up with you."
            )

        if state == "order_draft_created":
            return (
                "✅ Your item has been added to a draft order.\n\n"
                "We will show your order summary and next payment step shortly."
            )

        return (
            f"Welcome to {display_name}.\n\n"
            "Type *menu* to see products or *help* for assistance."
        )
</file>

<file path="app/services/whatsapp_service.py">
from __future__ import annotations

import httpx
from fastapi import HTTPException, status

from app.utils.encryption import decrypt_value


class WhatsAppService:
    BASE_URL = "https://graph.facebook.com/v23.0"

    async def send_text_message(
        self,
        *,
        access_token_encrypted: str,
        phone_number_id: str,
        to: str,
        body: str,
    ) -> dict:
        access_token = decrypt_value(access_token_encrypted)

        url = f"{self.BASE_URL}/{phone_number_id}/messages"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": body,
            },
        }

        try:
            async with httpx.AsyncClient(timeout=20.0) as client:
                response = await client.post(url, headers=headers, json=payload)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Unable to send WhatsApp message at this time.",
            ) from exc
</file>

<file path="app/services/whatsapp_webhook_service.py">
from __future__ import annotations

from app.repositories.whatsapp_account_repository import WhatsAppAccountRepository
from app.schemas.whatsapp import IncomingWhatsAppMessage


class WhatsAppWebhookService:
    def __init__(self, whatsapp_account_repo: WhatsAppAccountRepository) -> None:
        self.whatsapp_account_repo = whatsapp_account_repo

    async def extract_messages(self, payload: dict) -> list[IncomingWhatsAppMessage]:
        normalized_messages: list[IncomingWhatsAppMessage] = []

        for entry in payload.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})
                metadata = value.get("metadata", {})
                phone_number_id = metadata.get("phone_number_id")

                if not phone_number_id:
                    continue

                whatsapp_account = await self.whatsapp_account_repo.get_by_phone_number_id(phone_number_id)
                if whatsapp_account is None or not whatsapp_account.is_active:
                    continue

                contacts = value.get("contacts", [])
                contact_name = None
                if contacts:
                    profile = contacts[0].get("profile", {})
                    contact_name = profile.get("name")

                for message in value.get("messages", []):
                    customer_number = message.get("from")
                    message_id = message.get("id")
                    message_type = message.get("type")

                    if not customer_number or not message_id or not message_type:
                        continue

                    text_body = None
                    if message_type == "text":
                        text_body = (message.get("text") or {}).get("body")

                    normalized_messages.append(
                        IncomingWhatsAppMessage(
                            business_id=whatsapp_account.business_id,
                            phone_number_id=phone_number_id,
                            customer_number=customer_number,
                            customer_name=contact_name,
                            message_id=message_id,
                            message_type=message_type,
                            text_body=text_body,
                            raw_payload=message,
                        )
                    )

        return normalized_messages
</file>

<file path="app/tests/__init__.py">

</file>

<file path="app/tests/conftest.py">

</file>

<file path="app/tests/test_auth.py">

</file>

<file path="app/tests/test_health.py">
from fastapi.testclient import TestClient

from app.main import app


def test_health_check() -> None:
    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "service" in body
</file>

<file path="app/tests/test_onboarding_status.py">
from fastapi.testclient import TestClient

from app.main import app


def test_onboarding_status() -> None:
    client = TestClient(app)
    response = client.get("/api/v1/onboarding/status")

    assert response.status_code == 200
    body = response.json()
    assert "message" in body
</file>

<file path="app/tests/test_orders.py">

</file>

<file path="app/tests/test_paystack_webhook.py">

</file>

<file path="app/tests/test_whatsapp_webhook.py">

</file>

<file path="app/utils/__init__.py">

</file>

<file path="app/utils/encryption.py">
from __future__ import annotations

from cryptography.fernet import Fernet, InvalidToken

from app.core.config import get_settings

settings = get_settings()
fernet = Fernet(settings.app_encryption_key.encode())


def encrypt_value(value: str) -> str:
    return fernet.encrypt(value.encode()).decode()


def decrypt_value(value: str) -> str:
    try:
        return fernet.decrypt(value.encode()).decode()
    except InvalidToken as exc:
        raise ValueError("Unable to decrypt stored secret.") from exc
</file>

<file path="app/utils/exceptions.py">
from __future__ import annotations


class WapBizError(Exception):
    pass


class ProviderConfigurationError(WapBizError):
    pass


class SignatureVerificationError(WapBizError):
    pass


class ConversationProcessingError(WapBizError):
    pass
</file>

<file path="app/utils/formatting.py">

</file>

<file path="app/utils/idempotency.py">
from __future__ import annotations


def normalize_external_event_id(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.strip()
    return normalized or None
</file>

<file path="app/utils/pagination.py">

</file>

<file path="app/utils/time.py">

</file>

<file path="app/workers/__init__.py">

</file>

<file path="app/workers/catalog_sync_jobs.py">

</file>

<file path="app/workers/notification_jobs.py">

</file>

<file path="app/workers/receipt_jobs.py">

</file>

<file path="app/workers/retry_jobs.py">

</file>

<file path="backend_setup.sh">
#!/usr/bin/env bash
set -euo pipefail

echo "Creating WapBiz backend structure..."

BASE_DIR="."

mkdir -p "$BASE_DIR"/app/core
mkdir -p "$BASE_DIR"/app/api/routes
mkdir -p "$BASE_DIR"/app/models
mkdir -p "$BASE_DIR"/app/schemas
mkdir -p "$BASE_DIR"/app/services
mkdir -p "$BASE_DIR"/app/repositories
mkdir -p "$BASE_DIR"/app/utils
mkdir -p "$BASE_DIR"/app/workers
mkdir -p "$BASE_DIR"/app/tests
mkdir -p "$BASE_DIR"/alembic/versions

touch "$BASE_DIR"/app/__init__.py
touch "$BASE_DIR"/app/core/__init__.py
touch "$BASE_DIR"/app/api/__init__.py
touch "$BASE_DIR"/app/api/routes/__init__.py
touch "$BASE_DIR"/app/models/__init__.py
touch "$BASE_DIR"/app/schemas/__init__.py
touch "$BASE_DIR"/app/services/__init__.py
touch "$BASE_DIR"/app/repositories/__init__.py
touch "$BASE_DIR"/app/utils/__init__.py
touch "$BASE_DIR"/app/workers/__init__.py
touch "$BASE_DIR"/app/tests/__init__.py

touch "$BASE_DIR"/.env
touch "$BASE_DIR"/.env.example
touch "$BASE_DIR"/.gitignore
touch "$BASE_DIR"/README.md
touch "$BASE_DIR"/requirements.txt
touch "$BASE_DIR"/pyproject.toml
touch "$BASE_DIR"/Dockerfile
touch "$BASE_DIR"/docker-compose.yml
touch "$BASE_DIR"/alembic.ini

touch "$BASE_DIR"/app/main.py

touch "$BASE_DIR"/app/core/config.py
touch "$BASE_DIR"/app/core/security.py
touch "$BASE_DIR"/app/core/database.py
touch "$BASE_DIR"/app/core/logging.py
touch "$BASE_DIR"/app/core/tenancy.py
touch "$BASE_DIR"/app/core/deps.py
touch "$BASE_DIR"/app/core/constants.py

touch "$BASE_DIR"/app/api/routes/health.py
touch "$BASE_DIR"/app/api/routes/auth.py
touch "$BASE_DIR"/app/api/routes/onboarding.py
touch "$BASE_DIR"/app/api/routes/businesses.py
touch "$BASE_DIR"/app/api/routes/catalog.py
touch "$BASE_DIR"/app/api/routes/customers.py
touch "$BASE_DIR"/app/api/routes/orders.py
touch "$BASE_DIR"/app/api/routes/receipts.py
touch "$BASE_DIR"/app/api/routes/metrics.py
touch "$BASE_DIR"/app/api/routes/whatsapp_webhooks.py
touch "$BASE_DIR"/app/api/routes/paystack_webhooks.py

touch "$BASE_DIR"/app/models/business.py
touch "$BASE_DIR"/app/models/business_user.py
touch "$BASE_DIR"/app/models/business_settings.py
touch "$BASE_DIR"/app/models/whatsapp_account.py
touch "$BASE_DIR"/app/models/payment_provider.py
touch "$BASE_DIR"/app/models/customer.py
touch "$BASE_DIR"/app/models/catalog_category.py
touch "$BASE_DIR"/app/models/catalog_item.py
touch "$BASE_DIR"/app/models/order.py
touch "$BASE_DIR"/app/models/order_item.py
touch "$BASE_DIR"/app/models/payment.py
touch "$BASE_DIR"/app/models/receipt.py
touch "$BASE_DIR"/app/models/conversation_session.py
touch "$BASE_DIR"/app/models/webhook_event.py
touch "$BASE_DIR"/app/models/audit_log.py

touch "$BASE_DIR"/app/schemas/auth.py
touch "$BASE_DIR"/app/schemas/business.py
touch "$BASE_DIR"/app/schemas/business_user.py
touch "$BASE_DIR"/app/schemas/business_settings.py
touch "$BASE_DIR"/app/schemas/whatsapp.py
touch "$BASE_DIR"/app/schemas/paystack.py
touch "$BASE_DIR"/app/schemas/catalog.py
touch "$BASE_DIR"/app/schemas/customer.py
touch "$BASE_DIR"/app/schemas/order.py
touch "$BASE_DIR"/app/schemas/payment.py
touch "$BASE_DIR"/app/schemas/receipt.py
touch "$BASE_DIR"/app/schemas/metrics.py
touch "$BASE_DIR"/app/schemas/common.py

touch "$BASE_DIR"/app/services/tenant_service.py
touch "$BASE_DIR"/app/services/auth_service.py
touch "$BASE_DIR"/app/services/onboarding_service.py
touch "$BASE_DIR"/app/services/whatsapp_service.py
touch "$BASE_DIR"/app/services/conversation_service.py
touch "$BASE_DIR"/app/services/catalog_service.py
touch "$BASE_DIR"/app/services/customer_service.py
touch "$BASE_DIR"/app/services/order_service.py
touch "$BASE_DIR"/app/services/payment_service.py
touch "$BASE_DIR"/app/services/receipt_service.py
touch "$BASE_DIR"/app/services/notification_service.py
touch "$BASE_DIR"/app/services/webhook_security_service.py
touch "$BASE_DIR"/app/services/metrics_service.py
touch "$BASE_DIR"/app/services/audit_service.py

touch "$BASE_DIR"/app/repositories/base.py
touch "$BASE_DIR"/app/repositories/business_repository.py
touch "$BASE_DIR"/app/repositories/business_user_repository.py
touch "$BASE_DIR"/app/repositories/business_settings_repository.py
touch "$BASE_DIR"/app/repositories/whatsapp_account_repository.py
touch "$BASE_DIR"/app/repositories/payment_provider_repository.py
touch "$BASE_DIR"/app/repositories/customer_repository.py
touch "$BASE_DIR"/app/repositories/catalog_repository.py
touch "$BASE_DIR"/app/repositories/order_repository.py
touch "$BASE_DIR"/app/repositories/payment_repository.py
touch "$BASE_DIR"/app/repositories/receipt_repository.py
touch "$BASE_DIR"/app/repositories/conversation_session_repository.py
touch "$BASE_DIR"/app/repositories/webhook_event_repository.py
touch "$BASE_DIR"/app/repositories/audit_log_repository.py

touch "$BASE_DIR"/app/utils/idempotency.py
touch "$BASE_DIR"/app/utils/formatting.py
touch "$BASE_DIR"/app/utils/time.py
touch "$BASE_DIR"/app/utils/exceptions.py
touch "$BASE_DIR"/app/utils/encryption.py
touch "$BASE_DIR"/app/utils/pagination.py

touch "$BASE_DIR"/app/workers/receipt_jobs.py
touch "$BASE_DIR"/app/workers/notification_jobs.py
touch "$BASE_DIR"/app/workers/retry_jobs.py
touch "$BASE_DIR"/app/workers/catalog_sync_jobs.py

touch "$BASE_DIR"/app/tests/conftest.py
touch "$BASE_DIR"/app/tests/test_health.py
touch "$BASE_DIR"/app/tests/test_auth.py
touch "$BASE_DIR"/app/tests/test_orders.py
touch "$BASE_DIR"/app/tests/test_paystack_webhook.py
touch "$BASE_DIR"/app/tests/test_whatsapp_webhook.py

touch "$BASE_DIR"/alembic/env.py
touch "$BASE_DIR"/alembic/script.py.mako

echo "Backend structure created successfully."
</file>

<file path="docker-compose.yml">

</file>

<file path="Dockerfile">

</file>

<file path="pyproject.toml">
[tool.ruff]
line-length = 100
target-version = "py313"
exclude = [
  ".git",
  ".ruff_cache",
  ".pytest_cache",
  ".venv",
  "venv",
  "alembic/versions",
]

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP", "N", "ASYNC", "C4", "SIM"]
ignore = ["B008"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

[tool.pytest.ini_options]
pythonpath = ["."]
asyncio_mode = "auto"
testpaths = ["app/tests"]

[tool.coverage.run]
source = ["app"]

[tool.coverage.report]
omit = ["app/tests/*"]
show_missing = true
skip_covered = true
</file>

<file path="README.md">
# WapBiz Backend

This backend powers a multi-tenant WhatsApp-first business automation platform.

## Backend v1 foundation status
Implemented:

- FastAPI app setup
- environment-based settings
- structured logging
- async SQLAlchemy database layer
- business setup flow
- owner auth/session foundation
- WhatsApp webhook verification route
- WhatsApp webhook ingestion route
- Paystack webhook ingestion route
- conversation session foundation
- inbound/outbound message logging
- encrypted provider secret storage
- webhook signature verification foundation
- catalog category and item models
- order draft flow
- payment provider model
- payment initialization flow
- receipt generation foundation

## Important note
The codebase can be built before Supabase is connected.

You only need a running PostgreSQL database when you want to:

- generate/apply migrations
- create real DB records
- test onboarding against persistent storage
- test session/order/payment flows end-to-end

## Local development flow
1. Update `.env`
2. Run the backend
3. Confirm:
   - `/`
   - `/health`
   - `/api/v1/onboarding/status`
   - `/docs`

## Migration commands for later
When PostgreSQL or Supabase is ready:

```bash
alembic revision --autogenerate -m "create initial backend v1 tables"
alembic upgrade head
```

## Current scope
This is a WhatsApp-first commerce backend for:

- business onboarding
- tenant-aware business isolation
- WhatsApp webhook processing
- catalog browsing
- order draft creation
- payment initialization
- receipt generation
- later dashboard support
</file>

<file path="requirements.txt">
fastapi==0.135.3
uvicorn[standard]==0.44.0
sqlalchemy[asyncio]==2.0.44
psycopg[binary]==3.2.12
alembic==1.18.4
pydantic==2.13.0
pydantic-settings==2.13.1
httpx==0.28.1
PyJWT==2.12.1
pwdlib[argon2]==0.3.0
argon2-cffi==25.1.0
python-multipart==0.0.26
email-validator==2.3.0
structlog==25.5.0
tenacity==9.1.2
cryptography==45.0.7
pytest==8.4.2
pytest-asyncio==1.3.0
pytest-cov==7.0.0
ruff==0.15.10
</file>

</files>
