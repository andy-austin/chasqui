import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from chasqui.services.whatsapp import WhatsAppClient

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/messages", tags=["messages"])

wa_client = WhatsAppClient()


class TextMessageRequest(BaseModel):
    to: str
    body: str


class TemplateMessageRequest(BaseModel):
    to: str
    template_name: str
    language_code: str = "es"
    components: list[dict] | None = None


class DocumentMessageRequest(BaseModel):
    to: str
    document_url: str
    filename: str
    caption: str | None = None


@router.post("/send/text")
async def send_text(req: TextMessageRequest) -> dict:
    """Send a plain text WhatsApp message."""
    try:
        result = await wa_client.send_text_message(to=req.to, body=req.body)
    except Exception as exc:
        logger.error("Failed to send text message: %s", exc)
        raise HTTPException(status_code=502, detail="Failed to send message via WhatsApp API")
    return result


@router.post("/send/template")
async def send_template(req: TemplateMessageRequest) -> dict:
    """Send a pre-approved template message (can initiate conversations)."""
    try:
        result = await wa_client.send_template_message(
            to=req.to,
            template_name=req.template_name,
            language_code=req.language_code,
            components=req.components,
        )
    except Exception as exc:
        logger.error("Failed to send template message: %s", exc)
        raise HTTPException(status_code=502, detail="Failed to send message via WhatsApp API")
    return result


@router.post("/send/document")
async def send_document(req: DocumentMessageRequest) -> dict:
    """Send a document (e.g. PDF report) via WhatsApp."""
    try:
        result = await wa_client.send_document_message(
            to=req.to,
            document_url=req.document_url,
            filename=req.filename,
            caption=req.caption,
        )
    except Exception as exc:
        logger.error("Failed to send document message: %s", exc)
        raise HTTPException(status_code=502, detail="Failed to send message via WhatsApp API")
    return result
