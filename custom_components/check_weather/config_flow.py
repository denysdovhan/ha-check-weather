"""Adds config flow for Check Weather."""

import logging

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant import config_entries, data_entry_flow
from homeassistant.components.weather import (
    DOMAIN as WEATHER_DOMAIN,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.selector import selector

from .const import (
    CONF_HOURS,
    CONF_PREC_THRESHOLD,
    CONF_TEMP_THRESHOLD,
    CONF_WEATHER,
    CONF_WIND_THRESHOLD,
    DEFAULT_HOURS,
    DEFAULT_PREC_THRESHOLD,
    DEFAULT_TEMP_THRESHOLD,
    DEFAULT_WIND_THRESHOLD,
    DOMAIN,
    NAME,
)

LOGGER = logging.getLogger(__name__)


def get_config_value(
    entry: config_entries.ConfigEntry | None,
    key: str,
    default: any | None = None,
) -> any:
    """Get a value from the config entry or default."""
    if entry is not None:
        return entry.options.get(key, entry.data.get(key, default))
    return default


async def build_schema(
    config_entry: config_entries.ConfigEntry | None,
    hass: HomeAssistant,
) -> vol.Schema:
    """Build configuration schema."""
    # Fetch weather entities asynchronously
    weather_entities = list(hass.states.async_entity_ids(WEATHER_DOMAIN))
    suggested_weather = weather_entities[0] if weather_entities else None
    LOGGER.debug("Weather entities: %s", weather_entities)

    return vol.Schema(
        {
            vol.Required(
                CONF_WEATHER,
                default=get_config_value(config_entry, CONF_WEATHER, suggested_weather),
            ): selector(
                {
                    "entity": {
                        "include_entities": weather_entities,
                    },
                },
            ),
            vol.Optional(
                CONF_HOURS,
                default=get_config_value(config_entry, CONF_HOURS, DEFAULT_HOURS),
            ): cv.positive_int,
            vol.Optional(
                CONF_TEMP_THRESHOLD,
                default=get_config_value(
                    config_entry,
                    CONF_TEMP_THRESHOLD,
                    DEFAULT_TEMP_THRESHOLD,
                ),
            ): cv.positive_float,
            vol.Optional(
                CONF_PREC_THRESHOLD,
                default=get_config_value(
                    config_entry,
                    CONF_PREC_THRESHOLD,
                    DEFAULT_PREC_THRESHOLD,
                ),
            ): cv.positive_float,
            vol.Optional(
                CONF_WIND_THRESHOLD,
                default=get_config_value(
                    config_entry,
                    CONF_WIND_THRESHOLD,
                    DEFAULT_WIND_THRESHOLD,
                ),
            ): cv.positive_float,
        },
    )


class CheckWeatherOptionsFlow(config_entries.OptionsFlow):
    """Handle a change to options for an entry."""

    def __init__(self, config_entry: dict) -> None:
        """Initialize the options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self,
        user_input: dict | None = None,
    ) -> data_entry_flow.FlowResult:
        """Handle a flow initialized by the user."""
        if user_input is not None:
            LOGGER.debug("Updating options: %s", user_input)
            return self.async_create_entry(title="", data=user_input)

        data_schema = await build_schema(config_entry=self.config_entry, hass=self.hass)
        return self.async_show_form(step_id="init", data_schema=data_schema)


class CheckWeatherConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a configuration flow for a new entry."""

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: dict) -> CheckWeatherOptionsFlow:
        """Get the options flow for this handler."""
        return CheckWeatherOptionsFlow(config_entry)

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> data_entry_flow.FlowResult:
        """Handle the initial step."""
        if user_input is not None:
            # Validate and store the user input
            return self.async_create_entry(title=NAME, data=user_input)

        data_schema = await build_schema(config_entry=None, hass=self.hass)
        return self.async_show_form(step_id="user", data_schema=data_schema)
