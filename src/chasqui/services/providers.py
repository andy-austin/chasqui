from __future__ import annotations

from datetime import datetime
from typing import Any, Protocol

from pydantic import BaseModel


class ChannelEvent(BaseModel):
    """Normalized webhook event produced by any channel provider."""

    event_type: str
    message_id: str
    timestamp: datetime
    channel: str


class ChannelProvider(Protocol):
    """Interface that every communication-channel provider must satisfy."""

    async def send(self, to: str, content: dict[str, Any]) -> dict[str, Any]:
        """Transmit a message and return the provider-specific response."""
        ...

    async def parse_webhook(self, payload: dict[str, Any]) -> list[ChannelEvent]:
        """Convert a raw incoming webhook payload into normalized events."""
        ...

    async def health_check(self) -> bool:
        """Return True when the external API is reachable and healthy."""
        ...
