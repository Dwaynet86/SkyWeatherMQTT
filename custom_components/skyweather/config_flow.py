"""Config flow for Sky Weather."""
import logging

import voluptuous as vol
from homeassistant import config_entries, core, exceptions
from homeassistant.core import callback

_LOGGER = logging.getLogger(__name__)

async def validate_input(hass: core.HomeAssistant, data):
    """Validate user input."""
    for entry in hass.config_entries.async_entries(DOMAIN):
        if entry.data[CONF_PORT] == data[CONF_PORT]:
            raise AlreadyConfigured
    return {"title": f"Sky Weather topic {data[CONF_PORT]}"}
  
class skyweatherConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for the Ecowitt."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_UNKNOWN

    async def async_step_import(self, device_config):
        """Import a configuration.yaml config, if any."""
        try:
            await validate_input(self.hass, device_config)
        except AlreadyConfigured:
            return self.async_abort(reason="already_configured")

        port = device_config[CONF_PORT]
        return self.async_create_entry(
            title=f"Ecowitt on port {port}",
            data=device_config
        )
      async def async_step_user(self, user_input=None):
        """Give initial instructions for setup."""
        if user_input is not None:
            return await self.async_step_initial_options()

        return self.async_show_form(step_id="user")

    async def async_step_initial_options(self, user_input=None):
        """Ask the user for the setup options."""
        errors = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
                return self.async_create_entry(title=info["title"],
                                               data=user_input)
            except AlreadyConfigured:
                return self.async_abort(reason="already_configured")

        return self.async_show_form(
            step_id="initial_options", data_schema=DATA_SCHEMA, errors=errors
        )
