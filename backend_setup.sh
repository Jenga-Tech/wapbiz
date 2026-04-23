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