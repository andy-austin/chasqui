from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient

from tests.conftest import make_expired_token, make_token


@pytest.mark.asyncio
async def test_send_text_message(client: AsyncClient, auth_header: dict):
    mock_response = {"messaging_product": "whatsapp", "messages": [{"id": "wamid.xxx"}]}
    with patch(
        "chasqui.routes.messages.wa_client.send_text_message",
        new_callable=AsyncMock,
        return_value=mock_response,
    ):
        response = await client.post(
            "/messages/send/text",
            json={"to": "59894946990", "body": "Hola, tu vehículo está listo"},
            headers=auth_header,
        )
    assert response.status_code == 200
    assert response.json() == mock_response


@pytest.mark.asyncio
async def test_send_template_message(client: AsyncClient, auth_header: dict):
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
            headers=auth_header,
        )
    assert response.status_code == 200
    assert response.json() == mock_response


@pytest.mark.asyncio
async def test_send_document_message(client: AsyncClient, auth_header: dict):
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
            headers=auth_header,
        )
    assert response.status_code == 200
    assert response.json() == mock_response


@pytest.mark.asyncio
async def test_send_text_message_api_error(client: AsyncClient, auth_header: dict):
    with patch(
        "chasqui.routes.messages.wa_client.send_text_message",
        new_callable=AsyncMock,
        side_effect=Exception("API error"),
    ):
        response = await client.post(
            "/messages/send/text",
            json={"to": "59894946990", "body": "test"},
            headers=auth_header,
        )
    assert response.status_code == 502


@pytest.mark.asyncio
async def test_send_text_message_missing_fields(client: AsyncClient, auth_header: dict):
    response = await client.post(
        "/messages/send/text", json={"to": "59894946990"}, headers=auth_header
    )
    assert response.status_code == 422


# --- Auth rejection tests ---


@pytest.mark.asyncio
async def test_no_token_returns_401(client: AsyncClient):
    """Request without Authorization header is rejected."""
    response = await client.post(
        "/messages/send/text",
        json={"to": "59894946990", "body": "test"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_invalid_token_returns_401(client: AsyncClient):
    """Request with a garbage token is rejected."""
    response = await client.post(
        "/messages/send/text",
        json={"to": "59894946990", "body": "test"},
        headers={"Authorization": "Bearer not-a-real-jwt"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"


@pytest.mark.asyncio
async def test_wrong_secret_returns_401(client: AsyncClient):
    """Token signed with a different secret is rejected."""
    bad_token = make_token(secret="wrong-secret")
    response = await client.post(
        "/messages/send/text",
        json={"to": "59894946990", "body": "test"},
        headers={"Authorization": f"Bearer {bad_token}"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_expired_token_returns_401(client: AsyncClient):
    """Expired token is rejected with a specific message."""
    token = make_expired_token()
    response = await client.post(
        "/messages/send/text",
        json={"to": "59894946990", "body": "test"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Token has expired"
