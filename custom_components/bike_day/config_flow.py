import logging

import voluptuous as vol
from homeassistant import config_entries
import homeassistant.helpers.config_validation as cv
from homeassistant.components.weather import (
    DOMAIN as WEATHER_DOMAIN,
)

from .const import (
    DEFAULT_PREC_THRESHOLD,
    DEFAULT_TEMP_THRESHOLD,
    DEFAULT_WIND_THRESHOLD,
    DOMAIN,
    CONF_HOURS,
    CONF_PREC_THRESHOLD,
    CONF_TEMP_THRESHOLD,
    CONF_WEATHER,
    CONF_WIND_THRESHOLD,
    DEFAULT_HOURS,
)

LOGGER = logging.getLogger(__name__)

USER_SCHEMA = vol.Schema(
    {
        # FIXME: Provide list of available weather entities
        vol.Required(CONF_WEATHER): cv.string,
        vol.Optional(CONF_HOURS, default=DEFAULT_HOURS): cv.positive_int,
        vol.Optional(
            CONF_TEMP_THRESHOLD, default=DEFAULT_TEMP_THRESHOLD
        ): cv.positive_float,
        vol.Optional(
            CONF_PREC_THRESHOLD, default=DEFAULT_PREC_THRESHOLD
        ): cv.positive_float,
        vol.Optional(
            CONF_WIND_THRESHOLD, default=DEFAULT_WIND_THRESHOLD
        ): cv.positive_float,
    }
)

class BikeDayConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        # Implement the user step of the config flow
        if user_input is not None:
            # Validate and store the user input
            LOGGER.debug('Domain is %s', DOMAIN)
            LOGGER.debug("User input: %s", user_input)
            return self.async_create_entry(title="Bike Day", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=USER_SCHEMA,
        )