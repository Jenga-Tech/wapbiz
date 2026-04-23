from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.auth import router as auth_router
from app.api.routes.businesses import router as businesses_router
from app.api.routes.catalog import router as catalog_router
from app.api.routes.customers import router as customers_router
from app.api.routes.health import router as health_router
from app.api.routes.metrics import router as metrics_router
from app.api.routes.onboarding import router as onboarding_router
from app.api.routes.orders import router as orders_router
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
app.include_router(catalog_router)
app.include_router(customers_router)
app.include_router(orders_router)
app.include_router(metrics_router)
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