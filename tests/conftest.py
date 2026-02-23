import os
from datetime import UTC, datetime, timedelta

import jwt

# Test secrets — set before importing anything that reads settings
TEST_JWT_SECRET = "test-jwt-secret-for-chasqui-32bytes!"
TEST_ADMIN_SECRET = "test-admin-secret"

os.environ.setdefault("WHATSAPP_API_TOKEN", "test-token")
os.environ.setdefault("WHATSAPP_PHONE_NUMBER_ID", "123456789")
os.environ.setdefault("WHATSAPP_VERIFY_TOKEN", "test-verify-token")
os.environ.setdefault("JWT_SECRET", TEST_JWT_SECRET)
os.environ.setdefault("ADMIN_SECRET", TEST_ADMIN_SECRET)

import pytest  # noqa: E402
from httpx import ASGITransport, AsyncClient  # noqa: E402

from chasqui.main import app  # noqa: E402


def make_token(sub: str = "test-client", days: int = 90, secret: str = TEST_JWT_SECRET) -> str:
    """Generate a valid JWT for tests."""
    now = datetime.now(UTC)
    return jwt.encode({"sub": sub, "iat": now, "exp": now + timedelta(days=days)}, secret, "HS256")


def make_expired_token(sub: str = "test-client", secret: str = TEST_JWT_SECRET) -> str:
    """Generate an expired JWT for tests."""
    now = datetime.now(UTC)
    return jwt.encode(
        {"sub": sub, "iat": now - timedelta(days=2), "exp": now - timedelta(days=1)},
        secret,
        "HS256",
    )


@pytest.fixture
def auth_header() -> dict[str, str]:
    return {"Authorization": f"Bearer {make_token()}"}


@pytest.fixture
def admin_header() -> dict[str, str]:
    return {"Authorization": f"Bearer {TEST_ADMIN_SECRET}"}


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
