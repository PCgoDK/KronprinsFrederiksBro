"""API client for My Integration."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from .bridge_schedule import get_next_opening, get_open_window, is_open_now


class MyIntegrationApiClient:
    """Small API client wrapper used by the coordinator."""

    async def async_get_status(self, now: datetime) -> dict[str, Any]:
        """Return current bridge state and next possible opening time."""
        window_start, window_end = get_open_window(now.date())

        return {
            "is_possible_opening_now": is_open_now(now),
            "next_possible_opening": get_next_opening(now),
            "calculated_at": now,
            "first_possible_opening": window_start.strftime("%H:%M"),
            "last_possible_opening": window_end.strftime("%H:%M"),
        }
