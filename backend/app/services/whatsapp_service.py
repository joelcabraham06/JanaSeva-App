import logging
import httpx
from typing import Dict, Any, List, Optional
from app.core.config import settings

logger = logging.getLogger(__name__)

class WhatsAppService:
    @property
    def token(self) -> str:
        return settings.WHATSAPP_TOKEN

    @property
    def phone_id(self) -> str:
        return settings.WHATSAPP_PHONE_NUMBER_ID

    @property
    def api_url(self) -> str:
        return f"{settings.WHATSAPP_API_URL}/{self.phone_id}/messages"

    async def send_text_message(self, recipient_phone: str, message_text: str) -> Dict[str, Any]:
        """
        Sends a standard text message over Meta WhatsApp Cloud API.
        If using mock token, logs message and returns success payload.
        """
        if self.token == "mock_whatsapp_token" or not self.token:
            logger.info(f"[MOCK WHATSAPP OUTGOING -> {recipient_phone}]: {message_text}")
            return {"status": "sent", "mock": True, "recipient": recipient_phone, "message": message_text}

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": recipient_phone,
            "type": "text",
            "text": {"body": message_text}
        }

        async with httpx.AsyncClient() as client:
            try:
                res = await client.post(self.api_url, json=payload, headers=headers, timeout=10.0)
                res.raise_for_status()
                logger.info(f"Successfully sent Meta WhatsApp message to {recipient_phone}")
                return res.json()
            except Exception as e:
                logger.error(f"Failed to send Meta WhatsApp API message to {recipient_phone}: {e}")
                if hasattr(e, 'response') and e.response is not None:
                    logger.error(f"Meta Error response: {e.response.text}")
                return {"status": "error", "detail": str(e)}

    async def send_interactive_buttons(
        self,
        recipient_phone: str,
        header_text: str,
        body_text: str,
        buttons: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """
        Sends interactive reply buttons (e.g. Language Selection or Readiness Yes/No).
        Format for buttons: [{"id": "btn_ml", "title": "Malayalam"}, ...]
        """
        if self.token == "mock_whatsapp_token" or not self.token:
            logger.info(f"[MOCK WHATSAPP BUTTONS -> {recipient_phone}]: {body_text} | Buttons: {buttons}")
            return {"status": "sent", "mock": True, "recipient": recipient_phone, "buttons": buttons}

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        formatted_buttons = [
            {
                "type": "reply",
                "reply": {
                    "id": btn["id"],
                    "title": btn["title"][:20]  # Meta limit 20 chars
                }
            } for btn in buttons[:3] # Meta limit max 3 reply buttons
        ]

        payload = {
            "messaging_product": "whatsapp",
            "to": recipient_phone,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "header": {"type": "text", "text": header_text[:60]},
                "body": {"text": body_text},
                "action": {"buttons": formatted_buttons}
            }
        }

        async with httpx.AsyncClient() as client:
            try:
                res = await client.post(self.api_url, json=payload, headers=headers, timeout=10.0)
                res.raise_for_status()
                logger.info(f"Successfully sent Meta interactive buttons to {recipient_phone}")
                return res.json()
            except Exception as e:
                logger.error(f"Failed to send interactive WhatsApp buttons to {recipient_phone}: {e}")
                if hasattr(e, 'response') and e.response is not None:
                    logger.error(f"Meta Error response: {e.response.text}")
                return {"status": "error", "detail": str(e)}

whatsapp_service = WhatsAppService()
