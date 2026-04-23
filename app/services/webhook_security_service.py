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