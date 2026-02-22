import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_webhook_verification_success(client: AsyncClient):
    response = await client.get(
        "/webhook/whatsapp",
        params={
            "hub.mode": "subscribe",
            "hub.verify_token": "test-verify-token",
            "hub.challenge": "challenge_code_123",
        },
    )
    assert response.status_code == 200
    assert response.text == "challenge_code_123"


@pytest.mark.asyncio
async def test_webhook_verification_failure(client: AsyncClient):
    response = await client.get(
        "/webhook/whatsapp",
        params={
            "hub.mode": "subscribe",
            "hub.verify_token": "wrong_token",
            "hub.challenge": "challenge_code_123",
        },
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_receive_message(client: AsyncClient):
    payload = {
        "object": "whatsapp_business_account",
        "entry": [
            {
                "id": "BIZ_ACCOUNT_ID",
                "changes": [
                    {
                        "value": {
                            "messaging_product": "whatsapp",
                            "metadata": {
                                "display_phone_number": "59899000000",
                                "phone_number_id": "123456789",
                            },
                            "messages": [
                                {
                                    "from": "59899111111",
                                    "id": "wamid.abc123",
                                    "timestamp": "1709000000",
                                    "type": "text",
                                    "text": {"body": "Hola, quiero agendar"},
                                }
                            ],
                        },
                        "field": "messages",
                    }
                ],
            }
        ],
    }
    response = await client.post("/webhook/whatsapp", json=payload)
    assert response.status_code == 200
    assert response.json() == {"status": "received"}
