from datetime import datetime, timedelta
from datetime import timezone
from types import SimpleNamespace

from custom_components.kronprins_frederiks_bro.sensor import MyIntegrationMinutesUntilNextOpeningSensor


TZ = timezone(timedelta(hours=2))


class _Entry:
    entry_id = "entry-id"
    title = "Integration"
    options = {}


def test_minutes_until_next_opening_rounds_up(monkeypatch):
    current_time = datetime(2026, 6, 8, 11, 5, 10, tzinfo=TZ)
    next_opening = current_time + timedelta(minutes=24, seconds=50)
    coordinator = SimpleNamespace(
        data={"next_possible_opening": next_opening, "first_possible_opening": "09:00", "last_possible_opening": "14:30"}
    )
    sensor = MyIntegrationMinutesUntilNextOpeningSensor(_Entry(), coordinator)

    monkeypatch.setattr(
        "custom_components.kronprins_frederiks_bro.sensor.dt_util.now",
        lambda: current_time,
    )

    assert sensor.native_value == 25