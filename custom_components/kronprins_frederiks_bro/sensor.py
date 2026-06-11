"""Sensor platform for My Integration."""

from __future__ import annotations

from datetime import datetime

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.const import UnitOfTime
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import dt as dt_util

from .const import CONF_NAME, COORDINATOR, DOMAIN
from .coordinator import MyIntegrationDataUpdateCoordinator


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
            MyIntegrationNextOpeningSensor(entry, coordinator),
            MyIntegrationMinutesUntilNextOpeningSensor(entry, coordinator),
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
    def extra_state_attributes(self) -> dict[str, str]:
        """Explain that green periods represent possible openings only."""
        return {
            "opening_policy": "possible_only",
            "note": "Kun mulig åbning. Broen åbner ved behov, naar baade skal passere.",
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


class MyIntegrationNextOpeningSensor(
    CoordinatorEntity[MyIntegrationDataUpdateCoordinator], SensorEntity
):
    """Next possible opening timestamp sensor."""

    _attr_has_entity_name = True
    _attr_name = "Naeste mulige åbning"
    _attr_device_class = SensorDeviceClass.TIMESTAMP

    def __init__(
        self,
        entry: ConfigEntry,
        coordinator: MyIntegrationDataUpdateCoordinator,
    ) -> None:
        super().__init__(coordinator)
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_next_opening"

    @property
    def native_value(self) -> datetime | None:
        """Return next possible opening timestamp."""
        value = self.coordinator.data["next_possible_opening"]
        if isinstance(value, datetime):
            return value
        return None

    @property
    def extra_state_attributes(self) -> dict[str, str]:
        """Explain that timestamp is next possible opening slot."""
        return {
            "opening_policy": "possible_only",
            "note": "Tidsstemplet er naeste mulige åbningstid, ikke en garanteret åbning.",
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


class MyIntegrationMinutesUntilNextOpeningSensor(
    CoordinatorEntity[MyIntegrationDataUpdateCoordinator], SensorEntity
):
    """Minutes until next possible opening."""

    _attr_has_entity_name = True
    _attr_name = "Minutter til naeste mulige åbning"
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
        if delta.total_seconds() <= 0:
            return 0
        return int(delta.total_seconds() // 60)

    @property
    def device_info(self):
        """Return device information for grouping in Home Assistant."""
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": self._entry.options.get(CONF_NAME, self._entry.title),
            "manufacturer": "Custom",
            "model": "Template Integration",
        }
