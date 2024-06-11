import logging

import voluptuous as vol
from homeassistant.core import HomeAssistant, callback
from homeassistant import config_entries
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.selector import selector
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
    NAME,
)

LOGGER = logging.getLogger(__name__)

def get_config_value(entry: config_entries.ConfigEntry | None, key: str, default=None):
    """Get a value from the config entry or default."""
    if entry is not None:
        return entry.options.get(key, entry.data.get(key, default))
    else:
        return default

async def build_schema(config_entry: config_entries.ConfigEntry | None, hass: HomeAssistant):
    """Build configuration schema."""
    
    # Fetch weather entities asynchronously
    weather_entities = [
        entity_id for entity_id in hass.states.async_entity_ids(WEATHER_DOMAIN)
    ]
    LOGGER.debug('Weather entities: %s', weather_entities)

    return vol.Schema(
        {
            vol.Required(
                CONF_WEATHER,
                default=get_config_value(config_entry, CONF_WEATHER, weather_entities[0] if weather_entities else None),
            ): selector(
                {
                    "entity": {
                        "include_entities": weather_entities,
                    }
                }
            ),
            vol.Optional(
                CONF_HOURS,
                default=get_config_value(config_entry, CONF_HOURS, DEFAULT_HOURS),
            ): cv.positive_int,
            vol.Optional(
                CONF_TEMP_THRESHOLD,
                default=get_config_value(config_entry, CONF_TEMP_THRESHOLD, DEFAULT_TEMP_THRESHOLD),
            ): cv.positive_float,
            vol.Optional(
                CONF_PREC_THRESHOLD,
                default=get_config_value(config_entry, CONF_PREC_THRESHOLD, DEFAULT_PREC_THRESHOLD)
            ): cv.positive_float,
            vol.Optional(
                CONF_WIND_THRESHOLD,
                default=get_config_value(config_entry, CONF_WIND_THRESHOLD, DEFAULT_WIND_THRESHOLD)
            ): cv.positive_float,
        }
    )

class CheckWeatherConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a configuration flow for a new entry."""

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return CheckWeatherOptionsFlow(config_entry)

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""

        if user_input is not None:
            # Validate and store the user input
            return self.async_create_entry(title=NAME, data=user_input)

        data_schema = await build_schema(
            config_entry=None,
            hass=self.hass
        );
        
        return self.async_show_form(
            step_id="user",
            data_schema=data_schema
        )

class CheckWeatherOptionsFlow(config_entries.OptionsFlow):
    """Handle a change to options for an entry."""

    def __init__(self, config_entry):
        """Initialize the options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            LOGGER.debug("Updating options: %s", user_input)
            return self.async_create_entry(title="", data=user_input)

        data_schema = await build_schema(
            config_entry=self.config_entry,
            hass=self.hass
        )

        return self.async_show_form(
            step_id="init",
            data_schema=data_schema
        )