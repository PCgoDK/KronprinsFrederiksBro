"""Data coordinator for My Integration."""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.util import dt as dt_util
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .api import MyIntegrationApiClient
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class MyIntegrationDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinate periodic data updates for the integration."""

    def __init__(self, hass: HomeAssistant, api: MyIntegrationApiClient) -> None:
        super().__init__(
            hass,
            logger=_LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=1),
        )
        self._api = api

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from API."""
        return await self._api.async_get_status(dt_util.now())
