from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.database import get_db_session
from app.repositories.business_repository import BusinessRepository
from app.repositories.message_log_repository import MessageLogRepository
from app.repositories.webhook_event_repository import WebhookEventRepository
from app.repositories.whatsapp_account_repository import WhatsAppAccountRepository
from app.schemas.whatsapp import ConversationSessionResponse
from app.services.conversation_query_service import ConversationQueryService
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


@router.get(
    "/api/v1/conversations/{business_id}",
    response_model=list[ConversationSessionResponse],
    summary="List conversation sessions for a business",
)
async def list_conversation_sessions(
    business_id: str,
    db: AsyncSession = Depends(get_db_session),
) -> list[ConversationSessionResponse]:
    service = ConversationQueryService(db)
    result = await service.list_sessions(business_id)
    return [ConversationSessionResponse(**item) for item in result]