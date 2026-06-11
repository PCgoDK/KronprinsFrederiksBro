from datetime import datetime
from zoneinfo import ZoneInfo

from custom_components.kronprins_frederiks_bro.api import MyIntegrationApiClient


async def test_async_get_status_returns_expected_shape():
    client = MyIntegrationApiClient()

    result = await client.async_get_status(datetime(2026, 1, 8, 12, 0, tzinfo=ZoneInfo("Europe/Copenhagen")))

    assert "is_possible_opening_now" in result
    assert "next_possible_opening" in result
    assert result["first_possible_opening"] == "09:00"
    assert result["last_possible_opening"] == "14:30"
