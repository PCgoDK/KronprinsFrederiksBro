from datetime import datetime
from zoneinfo import ZoneInfo

from custom_components.kronprins_frederiks_bro.bridge_schedule import get_next_opening

TZ = ZoneInfo("Europe/Copenhagen")


def test_next_opening_skips_closed_monday_morning():
    now = datetime(2026, 6, 8, 8, 15, tzinfo=TZ)

    result = get_next_opening(now)

    assert result == datetime(2026, 6, 8, 9, 0, tzinfo=TZ)


def test_next_opening_during_midday_closure():
    now = datetime(2026, 6, 8, 14, 5, tzinfo=TZ)

    result = get_next_opening(now)

    assert result == datetime(2026, 6, 8, 14, 30, tzinfo=TZ)


def test_next_opening_returns_now_when_open():
    now = datetime(2026, 6, 8, 11, 10, tzinfo=TZ)

    result = get_next_opening(now)

    assert result == now


def test_next_opening_thursday_afternoon_gap():
    now = datetime(2026, 6, 11, 15, 12, tzinfo=TZ)

    result = get_next_opening(now)

    assert result == datetime(2026, 6, 11, 17, 30, tzinfo=TZ)


def test_next_opening_friday_afternoon_gap():
    now = datetime(2026, 6, 12, 15, 12, tzinfo=TZ)

    result = get_next_opening(now)

    assert result == datetime(2026, 6, 12, 16, 30, tzinfo=TZ)


def test_next_opening_weekend_midday_alternating_closure():
    now = datetime(2026, 6, 14, 12, 35, tzinfo=TZ)

    result = get_next_opening(now)

    assert result == datetime(2026, 6, 14, 13, 0, tzinfo=TZ)


def test_next_opening_respects_winter_small_window_start():
    now = datetime(2026, 1, 8, 8, 55, tzinfo=TZ)

    result = get_next_opening(now)

    assert result == datetime(2026, 1, 8, 9, 0, tzinfo=TZ)
