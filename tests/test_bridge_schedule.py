from datetime import datetime
from datetime import timezone, timedelta

from custom_components.kronprins_frederiks_bro.bridge_schedule import get_next_opening, is_open_now

TZ = timezone(timedelta(hours=2))


def test_next_opening_skips_closed_monday_morning():
    now = datetime(2026, 6, 8, 8, 15, tzinfo=TZ)

    result = get_next_opening(now)

    assert result == datetime(2026, 6, 8, 9, 0, tzinfo=TZ)


def test_next_opening_during_midday_closure():
    now = datetime(2026, 6, 8, 14, 5, tzinfo=TZ)

    result = get_next_opening(now)

    assert result == datetime(2026, 6, 8, 14, 30, tzinfo=TZ)


def test_next_opening_returns_current_slot_when_exact_open_time():
    now = datetime(2026, 6, 8, 11, 0, tzinfo=TZ)

    result = get_next_opening(now)

    assert result == now


def test_next_opening_skips_to_next_slot_five_minutes_after_open_time():
    now = datetime(2026, 6, 8, 11, 5, tzinfo=TZ)

    result = get_next_opening(now)

    assert result == datetime(2026, 6, 8, 11, 30, tzinfo=TZ)


def test_next_opening_skips_to_next_slot_five_minutes_after_half_past():
    now = datetime(2026, 6, 8, 11, 35, tzinfo=TZ)

    result = get_next_opening(now)

    assert result == datetime(2026, 6, 8, 12, 0, tzinfo=TZ)


def test_next_opening_thursday_afternoon_gap():
    now = datetime(2026, 6, 11, 15, 12, tzinfo=TZ)

    result = get_next_opening(now)

    assert result == datetime(2026, 6, 11, 17, 30, tzinfo=TZ)


def test_next_opening_friday_afternoon_gap():
    now = datetime(2026, 6, 12, 15, 12, tzinfo=TZ)

    result = get_next_opening(now)

    assert result == datetime(2026, 6, 12, 16, 30, tzinfo=TZ)


def test_is_open_now_friday_exact_slot_but_not_fifteen_minutes_later():
    assert is_open_now(datetime(2026, 6, 12, 10, 30, tzinfo=TZ)) is True
    assert is_open_now(datetime(2026, 6, 12, 10, 34, tzinfo=TZ)) is True
    assert is_open_now(datetime(2026, 6, 12, 10, 35, tzinfo=TZ)) is False
    assert is_open_now(datetime(2026, 6, 12, 10, 45, tzinfo=TZ)) is False


def test_next_opening_weekend_midday_alternating_closure():
    now = datetime(2026, 6, 14, 12, 35, tzinfo=TZ)

    result = get_next_opening(now)

    assert result == datetime(2026, 6, 14, 13, 0, tzinfo=TZ)


def test_next_opening_respects_winter_small_window_start():
    now = datetime(2026, 1, 8, 8, 55, tzinfo=TZ)

    result = get_next_opening(now)

    assert result == datetime(2026, 1, 8, 9, 0, tzinfo=TZ)
