from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_send_text_message(client: AsyncClient):
    mock_response = {"messaging_product": "whatsapp", "messages": [{"id": "wamid.xxx"}]}
    with patch(
        "chasqui.routes.messages.wa_client.send_text_message",
        new_callable=AsyncMock,
        return_value=mock_response,
    ):
        response = await client.post(
            "/messages/send/text",
            json={"to": "59894946990", "body": "Hola, tu vehículo está listo"},
        )
    assert response.status_code == 200
    assert response.json() == mock_response


@pytest.mark.asyncio
async def test_send_template_message(client: AsyncClient):
    mock_response = {"messaging_product": "whatsapp", "messages": [{"id": "wamid.xxx"}]}
    with patch(
        "chasqui.routes.messages.wa_client.send_template_message",
        new_callable=AsyncMock,
        return_value=mock_response,
    ):
        response = await client.post(
            "/messages/send/template",
            json={
                "to": "59894946990",
                "template_name": "hello_world",
                "language_code": "en_US",
            },
        )
    assert response.status_code == 200
    assert response.json() == mock_response


@pytest.mark.asyncio
async def test_send_document_message(client: AsyncClient):
    mock_response = {"messaging_product": "whatsapp", "messages": [{"id": "wamid.xxx"}]}
    with patch(
        "chasqui.routes.messages.wa_client.send_document_message",
        new_callable=AsyncMock,
        return_value=mock_response,
    ):
        response = await client.post(
            "/messages/send/document",
            json={
                "to": "59894946990",
                "document_url": "https://example.com/report.pdf",
                "filename": "report.pdf",
                "caption": "Tu reporte",
            },
        )
    assert response.status_code == 200
    assert response.json() == mock_response


@pytest.mark.asyncio
async def test_send_text_message_api_error(client: AsyncClient):
    with patch(
        "chasqui.routes.messages.wa_client.send_text_message",
        new_callable=AsyncMock,
        side_effect=Exception("API error"),
    ):
        response = await client.post(
            "/messages/send/text",
            json={"to": "59894946990", "body": "test"},
        )
    assert response.status_code == 502


@pytest.mark.asyncio
async def test_send_text_message_missing_fields(client: AsyncClient):
    response = await client.post("/messages/send/text", json={"to": "59894946990"})
    assert response.status_code == 422
