import os

# Set required env vars before importing anything that reads settings
os.environ.setdefault("WHATSAPP_API_TOKEN", "test-token")
os.environ.setdefault("WHATSAPP_PHONE_NUMBER_ID", "123456789")
os.environ.setdefault("WHATSAPP_VERIFY_TOKEN", "test-verify-token")

import pytest
from httpx import ASGITransport, AsyncClient

from chasqui.main import app


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
