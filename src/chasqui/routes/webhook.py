import logging

from fastapi import APIRouter, Query, Request, Response

from chasqui.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/webhook", tags=["webhook"], include_in_schema=False)


@router.get("/whatsapp")
async def verify_webhook(
    hub_mode: str = Query(alias="hub.mode"),
    hub_verify_token: str = Query(alias="hub.verify_token"),
    hub_challenge: str = Query(alias="hub.challenge"),
) -> Response:
    """Webhook verification endpoint. Meta sends a GET request to validate ownership."""
    if hub_mode == "subscribe" and hub_verify_token == settings.whatsapp_verify_token:
        logger.info("Webhook verified successfully")
        return Response(content=hub_challenge, media_type="text/plain")

    logger.warning("Webhook verification failed: invalid token")
    return Response(content="Forbidden", status_code=403)


@router.post("/whatsapp")
async def receive_message(request: Request) -> dict[str, str]:
    """Receive incoming messages and status updates from WhatsApp."""
    payload = await request.json()
    logger.info("Received webhook payload: %s", payload)

    # Extract message data from the nested Meta payload structure
    for entry in payload.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})
            messages = value.get("messages", [])
            for message in messages:
                sender = message.get("from")
                msg_type = message.get("type")
                logger.info("Message from %s (type: %s)", sender, msg_type)

                if msg_type == "text":
                    text = message.get("text", {}).get("body", "")
                    logger.info("Text content: %s", text)

    return {"status": "received"}
