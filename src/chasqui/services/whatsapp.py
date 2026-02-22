import logging

import httpx

from chasqui.config import settings

logger = logging.getLogger(__name__)


class WhatsAppClient:
    """Client for the Meta WhatsApp Business Cloud API."""

    def __init__(self) -> None:
        self.base_url = settings.whatsapp_api_base_url
        self.phone_number_id = settings.whatsapp_phone_number_id
        self.headers = {
            "Authorization": f"Bearer {settings.whatsapp_api_token}",
            "Content-Type": "application/json",
        }

    @property
    def messages_url(self) -> str:
        return f"{self.base_url}/{self.phone_number_id}/messages"

    async def send_text_message(self, to: str, body: str) -> dict:
        """Send a plain text message to a WhatsApp number.

        Args:
            to: Recipient phone number in international format (e.g. "59899123456").
            body: The text content of the message.
        """
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "text",
            "text": {"preview_url": False, "body": body},
        }
        return await self._send(payload)

    async def send_template_message(
        self,
        to: str,
        template_name: str,
        language_code: str = "es",
        components: list[dict] | None = None,
    ) -> dict:
        """Send a pre-approved template message (can initiate conversations).

        Args:
            to: Recipient phone number in international format.
            template_name: The name of the approved template in Meta Business Manager.
            language_code: Language code for the template (default: Spanish).
            components: Optional template components (header, body, button parameters).
        """
        template: dict = {
            "name": template_name,
            "language": {"code": language_code},
        }
        if components:
            template["components"] = components

        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "template",
            "template": template,
        }
        return await self._send(payload)

    async def send_document_message(
        self, to: str, document_url: str, filename: str, caption: str | None = None
    ) -> dict:
        """Send a document (e.g. PDF vehicle report) via URL.

        Args:
            to: Recipient phone number in international format.
            document_url: Public URL of the document.
            filename: Display filename for the document.
            caption: Optional caption text shown with the document.
        """
        document: dict = {"link": document_url, "filename": filename}
        if caption:
            document["caption"] = caption

        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "document",
            "document": document,
        }
        return await self._send(payload)

    async def _send(self, payload: dict) -> dict:
        """Execute the API call to Meta."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.messages_url,
                headers=self.headers,
                json=payload,
            )

        if response.status_code != 200:
            logger.error(
                "WhatsApp API error %d: %s",
                response.status_code,
                response.text,
            )
            response.raise_for_status()

        data = response.json()
        logger.info("Message sent successfully: %s", data)
        return data
