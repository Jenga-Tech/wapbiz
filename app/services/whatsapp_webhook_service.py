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