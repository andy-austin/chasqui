import jwt
import pytest
from httpx import AsyncClient

from tests.conftest import TEST_JWT_SECRET


@pytest.mark.asyncio
async def test_create_token(client: AsyncClient, admin_header: dict):
    """Admin can issue a client token."""
    response = await client.post(
        "/auth/token",
        json={"client_id": "workshop-123", "expires_in_days": 30},
        headers=admin_header,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
    assert data["client_id"] == "workshop-123"
    assert "access_token" in data
    assert "expires_at" in data

    # Verify the issued token is valid
    payload = jwt.decode(data["access_token"], TEST_JWT_SECRET, algorithms=["HS256"])
    assert payload["sub"] == "workshop-123"


@pytest.mark.asyncio
async def test_create_token_default_expiry(client: AsyncClient, admin_header: dict):
    """Token defaults to 90 days when expires_in_days is omitted."""
    response = await client.post(
        "/auth/token",
        json={"client_id": "torke-backend"},
        headers=admin_header,
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_token_without_admin_secret(client: AsyncClient):
    """Request without admin secret is rejected."""
    response = await client.post(
        "/auth/token",
        json={"client_id": "workshop-123"},
    )
    assert response.status_code in (401, 403)


@pytest.mark.asyncio
async def test_create_token_wrong_admin_secret(client: AsyncClient):
    """Request with wrong admin secret is rejected."""
    response = await client.post(
        "/auth/token",
        json={"client_id": "workshop-123"},
        headers={"Authorization": "Bearer wrong-secret"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid admin secret"


@pytest.mark.asyncio
async def test_create_token_empty_client_id(client: AsyncClient, admin_header: dict):
    """Empty client_id is rejected by validation."""
    response = await client.post(
        "/auth/token",
        json={"client_id": "", "expires_in_days": 30},
        headers=admin_header,
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_issued_token_works_on_messages(client: AsyncClient, admin_header: dict):
    """End-to-end: issue a token then use it to call a protected endpoint."""
    from unittest.mock import AsyncMock, patch

    # Step 1: Issue a token
    token_resp = await client.post(
        "/auth/token",
        json={"client_id": "e2e-test"},
        headers=admin_header,
    )
    token = token_resp.json()["access_token"]

    # Step 2: Use it on /messages/send/text
    mock_response = {"messaging_product": "whatsapp", "messages": [{"id": "wamid.xxx"}]}
    with patch(
        "chasqui.routes.messages.wa_client.send_text_message",
        new_callable=AsyncMock,
        return_value=mock_response,
    ):
        response = await client.post(
            "/messages/send/text",
            json={"to": "59894946990", "body": "hello from e2e"},
            headers={"Authorization": f"Bearer {token}"},
        )
    assert response.status_code == 200
