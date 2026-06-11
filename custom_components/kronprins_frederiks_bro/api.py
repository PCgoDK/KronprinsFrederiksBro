"""API client for My Integration."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from .bridge_schedule import get_next_opening, is_open_now


class MyIntegrationApiClient:
    """Small API client wrapper used by the coordinator."""

    def __init__(self, host: str) -> None:
        self._host = host

    async def async_get_status(self, now: datetime) -> dict[str, Any]:
        """Return current bridge state and next possible opening time."""
        return {
            "is_possible_opening_now": is_open_now(now),
            "next_possible_opening": get_next_opening(now),
            "calculated_at": now,
            "host": self._host,
        }
