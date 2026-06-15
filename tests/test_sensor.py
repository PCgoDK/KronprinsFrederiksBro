from datetime import datetime, timedelta
from datetime import timezone
from types import SimpleNamespace

from custom_components.kronprins_frederiks_bro.sensor import (
    MyIntegrationFirstOpeningTimeSensor,
    MyIntegrationLastOpeningTimeSensor,
    MyIntegrationMinutesUntilNextOpeningSensor,
    MyIntegrationNextOpeningTimeSensor,
)


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


def test_next_opening_time_sensor_returns_hh_mm():
    next_opening = datetime(2026, 6, 8, 16, 30, tzinfo=TZ)
    coordinator = SimpleNamespace(
        data={"next_possible_opening": next_opening, "first_possible_opening": "09:00", "last_possible_opening": "14:30"}
    )
    sensor = MyIntegrationNextOpeningTimeSensor(_Entry(), coordinator)

    assert sensor.native_value == "16:30"


def test_first_opening_time_sensor_returns_first_window_time():
    coordinator = SimpleNamespace(
        data={
            "next_possible_opening": None,
            "first_possible_opening": "06:30",
            "last_possible_opening": "22:00",
        }
    )
    sensor = MyIntegrationFirstOpeningTimeSensor(_Entry(), coordinator)

    assert sensor.native_value == "06:30"


def test_last_opening_time_sensor_returns_last_window_time():
    coordinator = SimpleNamespace(
        data={
            "next_possible_opening": None,
            "first_possible_opening": "06:30",
            "last_possible_opening": "22:00",
        }
    )
    sensor = MyIntegrationLastOpeningTimeSensor(_Entry(), coordinator)

    assert sensor.native_value == "22:00"