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