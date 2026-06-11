"""Config flow for My Integration."""

from __future__ import annotations

import voluptuous as vol
from homeassistant.helpers import config_validation as cv

from homeassistant import config_entries
from homeassistant.core import callback

from .const import CONF_HOST, CONF_NAME, DEFAULT_NAME, DOMAIN


class MyIntegrationConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for My Integration."""

    VERSION = 1

    async def async_step_user(self, user_input: dict | None = None):
        """Handle the initial step."""
        if user_input is not None:
            await self.async_set_unique_id(user_input[CONF_HOST])
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title=user_input[CONF_NAME],
                data=user_input,
            )

        schema = vol.Schema(
            {
                vol.Required(CONF_NAME, default=DEFAULT_NAME): str,
                vol.Required(CONF_HOST): cv.string,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors={},
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Create the options flow."""
        return MyIntegrationOptionsFlow(config_entry)


class MyIntegrationOptionsFlow(config_entries.OptionsFlow):
    """Handle My Integration options."""

    def __init__(self, config_entry) -> None:
        self.config_entry = config_entry

    async def async_step_init(self, user_input: dict | None = None):
        """Manage integration options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        schema = vol.Schema(
            {
                vol.Optional(
                    CONF_NAME,
                    default=self.config_entry.options.get(
                        CONF_NAME,
                        self.config_entry.data.get(CONF_NAME, DEFAULT_NAME),
                    ),
                ): str,
                vol.Optional(
                    CONF_HOST,
                    default=self.config_entry.options.get(
                        CONF_HOST,
                        self.config_entry.data.get(CONF_HOST, ""),
                    ),
                ): cv.string,
            }
        )
        return self.async_show_form(step_id="init", data_schema=schema)
