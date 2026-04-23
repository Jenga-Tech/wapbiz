from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.catalog_repository import CatalogRepository
from app.repositories.conversation_session_repository import ConversationSessionRepository
from app.repositories.customer_repository import CustomerRepository
from app.repositories.message_log_repository import MessageLogRepository
from app.repositories.order_repository import OrderRepository
from app.schemas.payment import InitializePaymentRequest
from app.schemas.whatsapp import IncomingWhatsAppMessage
from app.services.catalog_service import CatalogService
from app.services.order_service import OrderService
from app.services.payment_service import PaymentService
from app.services.whatsapp_reply_service import WhatsAppReplyService


class ConversationService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.customer_repo = CustomerRepository(db)
        self.session_repo = ConversationSessionRepository(db)
        self.message_log_repo = MessageLogRepository(db)
        self.catalog_service = CatalogService(CatalogRepository(db))
        self.order_service = OrderService(db)
        self.order_repo = OrderRepository(db)
        self.payment_service = PaymentService(db)
        self.reply_service = WhatsAppReplyService()

    async def handle_incoming_message(self, message: IncomingWhatsAppMessage) -> dict:
        customer = await self.customer_repo.get_or_create(
            business_id=message.business_id,
            whatsapp_number=message.customer_number,
            display_name=message.customer_name,
        )

        session = await self.session_repo.get_or_create(
            business_id=message.business_id,
            customer_id=customer.id,
        )

        await self.message_log_repo.create(
            business_id=message.business_id,
            customer_id=customer.id,
            conversation_session_id=session.id,
            direction="inbound",
            message_type=message.message_type,
            text_body=message.text_body,
            external_message_id=message.message_id,
            payload=message.raw_payload,
        )

        next_state = session.current_state
        context_json = session.context_json or {}
        reply_text = self.reply_service.build_text_reply(state=next_state)

        if message.message_type == "text" and message.text_body:
            normalized_text = message.text_body.strip()
            lowered_text = normalized_text.lower()

            if lowered_text in {"hi", "hello", "hey", "start"}:
                next_state = "greeting"
                reply_text = self.reply_service.build_text_reply(state=next_state)

            elif lowered_text in {"menu", "catalog", "products"}:
                next_state = "catalog_browsing"
                catalog_result = await self.catalog_service.build_catalog_browse_result(
                    message.business_id
                )
                reply_text = catalog_result.message

            elif lowered_text in {"help", "human"}:
                next_state = "human_handoff_requested"
                reply_text = self.reply_service.build_text_reply(state=next_state)
                context_json = {
                    **context_json,
                    "human_handoff_requested": True,
                }

            elif lowered_text == "checkout":
                active_order_id = context_json.get("active_order_id")
                if not active_order_id:
                    order = await self.order_repo.get_active_draft_by_customer(
                        message.business_id,
                        customer.id,
                    )
                    if order is not None:
                        active_order_id = order.id

                customer_email = context_json.get("customer_email")
                if not active_order_id:
                    reply_text = (
                        "You do not have an active draft order yet.\n\n"
                        "Type *menu* to browse products first."
                    )
                elif not customer_email:
                    reply_text = (
                        "To continue checkout, please send your email address."
                    )
                    next_state = "awaiting_checkout_email"
                else:
                    payment_result = await self.payment_service.initialize_paystack_payment(
                        InitializePaymentRequest(
                            order_id=active_order_id,
                            customer_email=customer_email,
                        )
                    )
                    next_state = "pending_payment"
                    reply_text = (
                        "💳 Your payment link is ready.\n\n"
                        f"{payment_result['authorization_url']}\n\n"
                        "Complete payment, and we will confirm your receipt automatically."
                    )

            elif "@" in normalized_text and next_state == "awaiting_checkout_email":
                active_order_id = context_json.get("active_order_id")
                if not active_order_id:
                    reply_text = (
                        "No active draft order was found.\n\n"
                        "Type *menu* to start again."
                    )
                else:
                    context_json = {
                        **context_json,
                        "customer_email": normalized_text,
                    }
                    payment_result = await self.payment_service.initialize_paystack_payment(
                        InitializePaymentRequest(
                            order_id=active_order_id,
                            customer_email=normalized_text,
                        )
                    )
                    next_state = "pending_payment"
                    reply_text = (
                        "💳 Your payment link is ready.\n\n"
                        f"{payment_result['authorization_url']}\n\n"
                        "Complete payment, and we will confirm your receipt automatically."
                    )

            else:
                try:
                    draft_result = await self.order_service.create_or_update_draft_order_from_item_name(
                        business_id=message.business_id,
                        customer_id=customer.id,
                        item_name=normalized_text,
                        quantity=1,
                    )
                    next_state = "order_draft_created"
                    reply_text = (
                        f"✅ Added *{draft_result['item_name']}* to your draft order.\n\n"
                        f"Quantity: {draft_result['quantity']}\n"
                        f"Subtotal: {draft_result['currency']} {draft_result['subtotal']}\n\n"
                        "Reply with another product name to add more, or type *checkout* to continue."
                    )
                    context_json = {
                        **context_json,
                        "active_order_id": draft_result["order_id"],
                    }
                except HTTPException as exc:
                    if exc.status_code == 404:
                        reply_text = (
                            "I didn't understand that selection.\n\n"
                            "Type *menu* to view available products, or type *help* for assistance."
                        )
                    else:
                        raise

            context_json = {
                **context_json,
                "last_user_text": message.text_body,
            }

        await self.session_repo.update_state(
            session=session,
            current_state=next_state,
            context_json=context_json,
            last_incoming_message_id=message.message_id,
        )

        await self.db.flush()

        return {
            "business_id": message.business_id,
            "customer_id": customer.id,
            "session_id": session.id,
            "current_state": next_state,
            "message_type": message.message_type,
            "text_body": message.text_body,
            "reply_text": reply_text,
            "customer_number": message.customer_number,
            "phone_number_id": message.phone_number_id,
        }