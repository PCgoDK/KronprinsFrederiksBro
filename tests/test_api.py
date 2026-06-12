import asyncio
from datetime import datetime
from datetime import timezone, timedelta

from custom_components.kronprins_frederiks_bro.api import MyIntegrationApiClient


def test_async_get_status_returns_expected_shape():
    client = MyIntegrationApiClient()

    result = asyncio.run(
        client.async_get_status(datetime(2026, 1, 8, 12, 0, tzinfo=timezone(timedelta(hours=2))))
    )

    assert "is_possible_opening_now" in result
    assert "next_possible_opening" in result
    assert result["first_possible_opening"] == "09:00"
    assert result["last_possible_opening"] == "14:30"
