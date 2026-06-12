"""Opening schedule logic for Kronprins Frederiksbro."""

from __future__ import annotations

from datetime import date, datetime, time, timedelta

HALF_HOUR = timedelta(minutes=30)
OPENING_STATUS_WINDOW = timedelta(minutes=5)


def _t(value: str) -> time:
    hour, minute = value.split(":")
    return time(hour=int(hour), minute=int(minute))


WINDOWS: dict[str, dict[int, tuple[time, time]]] = {
    "mon_thu": {
        1: (_t("9:00"), _t("14:30")),
        2: (_t("9:00"), _t("17:30")),
        3: (_t("9:00"), _t("18:30")),
        4: (_t("9:00"), _t("20:30")),
        5: (_t("9:00"), _t("21:30")),
        6: (_t("9:00"), _t("22:00")),
        7: (_t("9:00"), _t("22:00")),
        8: (_t("9:00"), _t("21:00")),
        9: (_t("9:00"), _t("19:30")),
        10: (_t("9:00"), _t("18:30")),
        11: (_t("9:00"), _t("14:30")),
        12: (_t("9:00"), _t("14:30")),
    },
    "friday": {
        1: (_t("9:00"), _t("16:30")),
        2: (_t("9:00"), _t("17:30")),
        3: (_t("9:00"), _t("18:30")),
        4: (_t("9:00"), _t("20:30")),
        5: (_t("9:00"), _t("21:30")),
        6: (_t("9:00"), _t("22:00")),
        7: (_t("9:00"), _t("22:00")),
        8: (_t("9:00"), _t("21:00")),
        9: (_t("9:00"), _t("19:30")),
        10: (_t("9:00"), _t("18:30")),
        11: (_t("9:00"), _t("16:30")),
        12: (_t("9:00"), _t("13:30")),
    },
    "weekend_holiday": {
        1: (_t("8:00"), _t("16:30")),
        2: (_t("7:30"), _t("17:30")),
        3: (_t("6:30"), _t("18:30")),
        4: (_t("6:30"), _t("20:30")),
        5: (_t("6:30"), _t("21:30")),
        6: (_t("6:30"), _t("22:00")),
        7: (_t("6:30"), _t("22:00")),
        8: (_t("6:30"), _t("21:00")),
        9: (_t("6:30"), _t("19:30")),
        10: (_t("7:30"), _t("18:30")),
        11: (_t("7:30"), _t("16:30")),
        12: (_t("8:00"), _t("16:00")),
    },
}

CLOSED_SLOTS: dict[str, set[time]] = {
    "mon_thu": {
        _t("6:30"),
        _t("7:00"),
        _t("7:30"),
        _t("8:00"),
        _t("8:30"),
        _t("14:00"),
        _t("15:00"),
        _t("15:30"),
        _t("16:00"),
        _t("16:30"),
        _t("17:00"),
        _t("18:00"),
    },
    "friday": {
        _t("6:30"),
        _t("7:00"),
        _t("7:30"),
        _t("8:00"),
        _t("8:30"),
        _t("14:00"),
        _t("14:30"),
        _t("15:00"),
        _t("15:30"),
        _t("16:00"),
        _t("17:00"),
        _t("17:30"),
        _t("18:00"),
    },
    "weekend_holiday": {
        _t("10:30"),
        _t("11:30"),
        _t("12:30"),
        _t("13:30"),
    },
}


def _easter_sunday(year: int) -> date:
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return date(year, month, day)


def is_danish_holiday(day: date) -> bool:
    """Return True when day is a Danish public holiday."""
    easter = _easter_sunday(day.year)
    holidays = {
        date(day.year, 1, 1),
        easter - timedelta(days=3),
        easter - timedelta(days=2),
        easter,
        easter + timedelta(days=1),
        easter + timedelta(days=39),
        easter + timedelta(days=49),
        easter + timedelta(days=50),
        date(day.year, 12, 25),
        date(day.year, 12, 26),
    }
    return day in holidays


def _day_type(day: date) -> str:
    if day.weekday() >= 5 or is_danish_holiday(day):
        return "weekend_holiday"
    if day.weekday() == 4:
        return "friday"
    return "mon_thu"


def get_open_window(day: date) -> tuple[time, time]:
    """Return monthly first and last possible opening time for the day type."""
    day_type = _day_type(day)
    return WINDOWS[day_type][day.month]


def _floor_half_hour(moment: datetime) -> datetime:
    minute = 30 if moment.minute >= 30 else 0
    return moment.replace(minute=minute, second=0, microsecond=0)


def _ceil_half_hour(moment: datetime) -> datetime:
    floored = _floor_half_hour(moment)
    if floored == moment.replace(second=0, microsecond=0):
        return floored
    return floored + HALF_HOUR


def _is_exact_half_hour(moment: datetime) -> bool:
    return moment.second == 0 and moment.microsecond == 0 and moment.minute in {0, 30}


def _is_open_slot(slot: datetime) -> bool:
    day_type = _day_type(slot.date())
    start, end = get_open_window(slot.date())
    slot_time = slot.timetz().replace(tzinfo=None)

    if slot_time < start or slot_time > end:
        return False
    return slot_time not in CLOSED_SLOTS[day_type]


def is_open_now(moment: datetime) -> bool:
    """Return True if passing is possible in the first five minutes of a slot."""
    slot_start = _floor_half_hour(moment)
    if not _is_open_slot(slot_start):
        return False
    return moment - slot_start < OPENING_STATUS_WINDOW


def get_next_opening(moment: datetime, max_days: int = 14) -> datetime | None:
    """Return next possible opening time."""
    if is_open_now(moment):
        return moment

    candidate = _ceil_half_hour(moment)
    deadline = moment + timedelta(days=max_days)

    while candidate <= deadline:
        if _is_open_slot(candidate):
            return candidate
        candidate += HALF_HOUR

    return None
