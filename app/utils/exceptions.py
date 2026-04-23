from __future__ import annotations


class WapBizError(Exception):
    pass


class ProviderConfigurationError(WapBizError):
    pass


class SignatureVerificationError(WapBizError):
    pass


class ConversationProcessingError(WapBizError):
    pass