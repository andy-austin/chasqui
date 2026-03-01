"""Tests for the ChannelProvider protocol and ChannelEvent model."""

from datetime import UTC, datetime
from typing import Any

import pytest

from chasqui.services.providers import ChannelEvent, ChannelProvider, EventType


class _DummyProvider:
    """Minimal concrete implementation used to verify protocol compatibility."""

    async def send(self, to: str, content: dict[str, Any]) -> dict[str, Any]:
        return {"to": to, "content": content}

    async def parse_webhook(self, payload: dict[str, Any]) -> list[ChannelEvent]:
        return [
            ChannelEvent(
                event_type=EventType.MESSAGE,
                message_id=payload.get("id", "test-id"),
                timestamp=datetime.now(UTC),
                channel="dummy",
            )
        ]

    async def health_check(self) -> bool:
        return True


def test_dummy_provider_satisfies_protocol() -> None:
    provider: ChannelProvider = _DummyProvider()  # type: ignore[assignment]
    assert isinstance(provider, _DummyProvider)


@pytest.mark.asyncio
async def test_send_returns_dict() -> None:
    provider = _DummyProvider()
    result = await provider.send("123", {"text": "hello"})
    assert result == {"to": "123", "content": {"text": "hello"}}


@pytest.mark.asyncio
async def test_parse_webhook_returns_channel_events() -> None:
    provider = _DummyProvider()
    events = await provider.parse_webhook({"id": "msg-42"})
    assert len(events) == 1
    event = events[0]
    assert isinstance(event, ChannelEvent)
    assert event.event_type == EventType.MESSAGE
    assert event.message_id == "msg-42"
    assert event.channel == "dummy"


@pytest.mark.asyncio
async def test_health_check_returns_bool() -> None:
    provider = _DummyProvider()
    assert await provider.health_check() is True


def test_channel_event_fields() -> None:
    now = datetime.now(UTC)
    event = ChannelEvent(
        event_type=EventType.STATUS,
        message_id="wamid-xyz",
        timestamp=now,
        channel="whatsapp",
    )
    assert event.event_type == EventType.STATUS
    assert event.message_id == "wamid-xyz"
    assert event.timestamp == now
    assert event.channel == "whatsapp"
