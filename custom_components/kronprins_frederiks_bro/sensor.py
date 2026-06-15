"""Sensor platform for My Integration."""

from __future__ import annotations

import base64
from datetime import datetime
from pathlib import Path

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import UnitOfTime
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import dt as dt_util

from .const import CONF_NAME, COORDINATOR, DOMAIN
from .coordinator import MyIntegrationDataUpdateCoordinator


def _load_png_data_uri(image_path: Path) -> str | None:
    """Load a PNG as a data URI for use in entity_picture."""
    if not image_path.exists():
        return None

    try:
        encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
    except OSError:
        return None

    return f"data:image/png;base64,{encoded}"


_OPEN_POSSIBLE_IMAGE = _load_png_data_uri(
    Path(__file__).parent / "assets" / "oplukkelig-bro-vejskilt-advarselsskilt.png"
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensor entities from a config entry."""
    coordinator: MyIntegrationDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id][
        COORDINATOR
    ]
    async_add_entities(
        [
            MyIntegrationStatusSensor(entry, coordinator),
            MyIntegrationMinutesUntilNextOpeningSensor(entry, coordinator),
            MyIntegrationNextOpeningTimeSensor(entry, coordinator),
            MyIntegrationFirstOpeningTimeSensor(entry, coordinator),
            MyIntegrationLastOpeningTimeSensor(entry, coordinator),
        ]
    )


class MyIntegrationStatusSensor(CoordinatorEntity[MyIntegrationDataUpdateCoordinator], SensorEntity):
    """Possible opening status sensor."""

    _attr_has_entity_name = True
    _attr_name = "Mulig åbning status"

    def __init__(
        self,
        entry: ConfigEntry,
        coordinator: MyIntegrationDataUpdateCoordinator,
    ) -> None:
        super().__init__(coordinator)
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_status"

    @property
    def native_value(self) -> str:
        """Return current state from coordinator data."""
        return "mulig" if self.coordinator.data["is_possible_opening_now"] else "ikke_mulig"

    @property
    def icon(self) -> str:
        """Return icon for possible open or closed state."""
        if self.coordinator.data["is_possible_opening_now"]:
            return "mdi:bridge"
        return "mdi:bridge-lock"

    @property
    def entity_picture(self) -> str | None:
        """Show the user-provided picture when opening is currently possible."""
        if self.coordinator.data["is_possible_opening_now"]:
            return _OPEN_POSSIBLE_IMAGE
        return None

    @property
    def extra_state_attributes(self) -> dict[str, str]:
        """Explain that green periods represent possible openings only."""
        return {
            "opening_policy": "possible_only",
            "note": "Kun mulig åbning. Broen åbner ved behov, naar baade skal passere.",
            "dagens_forste_mulige": self.coordinator.data["first_possible_opening"],
            "dagens_sidste_mulige": self.coordinator.data["last_possible_opening"],
        }

    @property
    def device_info(self):
        """Return device information for the sensor."""
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": self._entry.options.get(CONF_NAME, self._entry.title),
            "manufacturer": "Custom",
            "model": "Template Integration",
        }


class MyIntegrationMinutesUntilNextOpeningSensor(
    CoordinatorEntity[MyIntegrationDataUpdateCoordinator], SensorEntity
):
    """Minutes until next possible opening."""

    _attr_has_entity_name = True
    _attr_name = "Næste mulige åbning"
    _attr_icon = "mdi:timer-sand"
    _attr_native_unit_of_measurement = UnitOfTime.MINUTES
    _attr_suggested_display_precision = 0

    def __init__(
        self,
        entry: ConfigEntry,
        coordinator: MyIntegrationDataUpdateCoordinator,
    ) -> None:
        super().__init__(coordinator)
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_minutes_until_next_possible_opening"

    @property
    def native_value(self) -> int | None:
        """Return minutes until the next possible opening slot."""
        next_opening = self.coordinator.data["next_possible_opening"]
        if not isinstance(next_opening, datetime):
            return None

        delta = next_opening - dt_util.now()
        seconds = delta.total_seconds()
        if seconds <= 0:
            return 0
        return int((seconds + 59) // 60)

    @property
    def extra_state_attributes(self) -> dict[str, str]:
        """Return explanatory attributes for countdown and seasonal window."""
        return {
            "opening_policy": "possible_only",
            "dagens_forste_mulige": self.coordinator.data["first_possible_opening"],
            "dagens_sidste_mulige": self.coordinator.data["last_possible_opening"],
        }

    @property
    def device_info(self):
        """Return device information for grouping in Home Assistant."""
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": self._entry.options.get(CONF_NAME, self._entry.title),
            "manufacturer": "Custom",
            "model": "Template Integration",
        }


class MyIntegrationNextOpeningTimeSensor(
    CoordinatorEntity[MyIntegrationDataUpdateCoordinator], SensorEntity
):
    """Clock time for the next possible opening."""

    _attr_has_entity_name = True
    _attr_name = "Næste åbning klokkeslæt"

    def __init__(
        self,
        entry: ConfigEntry,
        coordinator: MyIntegrationDataUpdateCoordinator,
    ) -> None:
        super().__init__(coordinator)
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_next_opening_time"

    @property
    def native_value(self) -> str | None:
        """Return the next opening as a clock time."""
        next_opening = self.coordinator.data["next_possible_opening"]
        if not isinstance(next_opening, datetime):
            return None

        return next_opening.strftime("%H:%M")

    @property
    def extra_state_attributes(self) -> dict[str, str]:
        """Return explanatory attributes for the next opening clock time."""
        return {
            "opening_policy": "possible_only",
            "dagens_forste_mulige": self.coordinator.data["first_possible_opening"],
            "dagens_sidste_mulige": self.coordinator.data["last_possible_opening"],
        }

    @property
    def device_info(self):
        """Return device information for grouping in Home Assistant."""
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": self._entry.options.get(CONF_NAME, self._entry.title),
            "manufacturer": "Custom",
            "model": "Template Integration",
        }


class MyIntegrationFirstOpeningTimeSensor(
    CoordinatorEntity[MyIntegrationDataUpdateCoordinator], SensorEntity
):
    """Clock time for the first possible opening today."""

    _attr_has_entity_name = True
    _attr_name = "Dagens første"
    _attr_icon = "mdi:clock-start"

    def __init__(
        self,
        entry: ConfigEntry,
        coordinator: MyIntegrationDataUpdateCoordinator,
    ) -> None:
        super().__init__(coordinator)
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_first_opening_time"

    @property
    def native_value(self) -> str | None:
        """Return today's first possible opening as a clock time."""
        first_opening = self.coordinator.data["first_possible_opening"]
        if not isinstance(first_opening, str):
            return None
        return first_opening

    @property
    def device_info(self):
        """Return device information for grouping in Home Assistant."""
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": self._entry.options.get(CONF_NAME, self._entry.title),
            "manufacturer": "Custom",
            "model": "Template Integration",
        }


class MyIntegrationLastOpeningTimeSensor(
    CoordinatorEntity[MyIntegrationDataUpdateCoordinator], SensorEntity
):
    """Clock time for the last possible opening today."""

    _attr_has_entity_name = True
    _attr_name = "Dagens sidste"
    _attr_icon = "mdi:clock-end"

    def __init__(
        self,
        entry: ConfigEntry,
        coordinator: MyIntegrationDataUpdateCoordinator,
    ) -> None:
        super().__init__(coordinator)
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_last_opening_time"

    @property
    def native_value(self) -> str | None:
        """Return today's last possible opening as a clock time."""
        last_opening = self.coordinator.data["last_possible_opening"]
        if not isinstance(last_opening, str):
            return None
        return last_opening

    @property
    def device_info(self):
        """Return device information for grouping in Home Assistant."""
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": self._entry.options.get(CONF_NAME, self._entry.title),
            "manufacturer": "Custom",
            "model": "Template Integration",
        }
