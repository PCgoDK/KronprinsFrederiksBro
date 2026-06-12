from __future__ import annotations

from types import ModuleType, SimpleNamespace
import sys


def _ensure_module(name: str) -> ModuleType:
    module = sys.modules.get(name)
    if module is None:
        module = ModuleType(name)
        sys.modules[name] = module
    return module


homeassistant = _ensure_module("homeassistant")
config_entries = _ensure_module("homeassistant.config_entries")
core = _ensure_module("homeassistant.core")
components = _ensure_module("homeassistant.components")
sensor = _ensure_module("homeassistant.components.sensor")
const = _ensure_module("homeassistant.const")
helpers = _ensure_module("homeassistant.helpers")
update_coordinator = _ensure_module("homeassistant.helpers.update_coordinator")
entity_platform = _ensure_module("homeassistant.helpers.entity_platform")
util = _ensure_module("homeassistant.util")
dt = _ensure_module("homeassistant.util.dt")

homeassistant.config_entries = config_entries
homeassistant.core = core
homeassistant.components = components
homeassistant.const = const
homeassistant.helpers = helpers
homeassistant.util = util
components.sensor = sensor
helpers.update_coordinator = update_coordinator
helpers.entity_platform = entity_platform
util.dt = dt


class ConfigEntry:
    def __init__(self, entry_id: str = "test-entry", title: str = "Test", options: dict | None = None) -> None:
        self.entry_id = entry_id
        self.title = title
        self.options = options or {}

    def add_update_listener(self, listener):
        return listener

    def async_on_unload(self, callback):
        return callback


class HomeAssistant:
    def __init__(self) -> None:
        self.data = {}
        self.config_entries = SimpleNamespace(
            async_forward_entry_setups=lambda *args, **kwargs: None,
            async_unload_platforms=lambda *args, **kwargs: True,
            async_reload=lambda *args, **kwargs: None,
        )


class SensorEntity:
    pass


class CoordinatorEntity:
    def __init__(self, coordinator) -> None:
        self.coordinator = coordinator

    @classmethod
    def __class_getitem__(cls, item):
        return cls


class DataUpdateCoordinator:
    def __init__(self, *args, **kwargs) -> None:
        pass

    @classmethod
    def __class_getitem__(cls, item):
        return cls


class AddEntitiesCallback:
    pass


class UnitOfTime:
    MINUTES = "min"


config_entries.ConfigEntry = ConfigEntry
core.HomeAssistant = HomeAssistant
sensor.SensorEntity = SensorEntity
update_coordinator.CoordinatorEntity = CoordinatorEntity
update_coordinator.DataUpdateCoordinator = DataUpdateCoordinator
entity_platform.AddEntitiesCallback = AddEntitiesCallback
const.UnitOfTime = UnitOfTime
dt.now = lambda: None