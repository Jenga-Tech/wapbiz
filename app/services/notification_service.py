from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.receipt import Receipt
from app.models.whatsapp_account import WhatsAppAccount
from app.repositories.business_repository import BusinessRepository
from app.repositories.message_log_repository import MessageLogRepository
from app.repositories.whatsapp_account_repository import WhatsAppAccountRepository
from app.services.whatsapp_service import WhatsAppService


class NotificationService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.business_repo = BusinessRepository(db)
        self.whatsapp_account_repo = WhatsAppAccountRepository(db)
        self.message_log_repo = MessageLogRepository(db)
        self.whatsapp_service = WhatsAppService()

    async def send_text_to_customer(
        self,
        *,
        business_id: str,
        customer_id: str | None,
        conversation_session_id: str | None,
        to: str,
        body: str,
        phone_number_id: str,
    ) -> dict | None:
        business, whatsapp_account = await self.business_repo.get_business_and_whatsapp_account(
            phone_number_id
        )
        if business is None or whatsapp_account is None or not whatsapp_account.access_token_encrypted:
            return None

        provider_response = await self.whatsapp_service.send_text_message(
            access_token_encrypted=whatsapp_account.access_token_encrypted,
            phone_number_id=phone_number_id,
            to=to,
            body=body,
        )

        outbound_message_id = None
        messages = provider_response.get("messages") or []
        if messages:
            outbound_message_id = messages[0].get("id")

        await self.message_log_repo.create(
            business_id=business_id,
            customer_id=customer_id,
            conversation_session_id=conversation_session_id,
            direction="outbound",
            message_type="text",
            text_body=body,
            external_message_id=outbound_message_id,
            status="sent",
            payload=provider_response,
        )

        return provider_response

    async def mark_receipt_customer_delivered(self, receipt: Receipt) -> None:
        receipt.customer_delivery_status = "sent"
        await self.db.flush()

    async def mark_receipt_owner_delivered(self, receipt: Receipt) -> None:
        receipt.owner_delivery_status = "sent"
        await self.db.flush()