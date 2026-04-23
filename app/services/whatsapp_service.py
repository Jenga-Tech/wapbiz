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