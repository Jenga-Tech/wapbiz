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