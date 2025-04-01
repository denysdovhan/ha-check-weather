"""Binary sensor platform for check_weather."""

from __future__ import annotations

import datetime as dt
import logging
from typing import TYPE_CHECKING, Any

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.components.weather import (
    ATTR_CONDITION_HAIL,
    ATTR_CONDITION_LIGHTNING,
    ATTR_CONDITION_LIGHTNING_RAINY,
    ATTR_CONDITION_POURING,
    ATTR_CONDITION_RAINY,
    ATTR_CONDITION_SNOWY,
    ATTR_CONDITION_SNOWY_RAINY,
    ATTR_FORECAST_CONDITION,
    ATTR_FORECAST_PRECIPITATION,
    ATTR_FORECAST_TEMP,
    ATTR_FORECAST_TIME,
    ATTR_FORECAST_WIND_SPEED,
    SERVICE_GET_FORECASTS,
)
from homeassistant.components.weather import (
    DOMAIN as WEATHER_DOMAIN,
)
from homeassistant.exceptions import HomeAssistantError
from homeassistant.util import dt as dt_util

from .const import (
    ATTR_BAD_WEATHER_TIME,
    ATTR_COLD_TEMPERATURE,
    ATTR_CONDITION,
    ATTR_HOT_TEMPERATURE,
    ATTR_PRECIPITATION,
    ATTR_STRONG_WIND,
    CONF_HOURS,
    CONF_MAX_TEMP,
    CONF_MIN_TEMP,
    CONF_PREC_THRESHOLD,
    CONF_WEATHER,
    CONF_WIND_THRESHOLD,
    DEFAULT_HOURS,
    DEFAULT_MAX_TEMP,
    DEFAULT_MIN_TEMP,
    DEFAULT_PREC_THRESHOLD,
    DEFAULT_WEATHER,
    DEFAULT_WIND_THRESHOLD,
    DOMAIN,
    ICON_OFF,
    ICON_ON,
    NAME,
)

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

LOGGER = logging.getLogger(__name__)

BAD_CONDITIONS = [
    ATTR_CONDITION_LIGHTNING,
    ATTR_CONDITION_LIGHTNING_RAINY,
    ATTR_CONDITION_HAIL,
    ATTR_CONDITION_RAINY,
    ATTR_CONDITION_SNOWY,
    ATTR_CONDITION_SNOWY_RAINY,
    ATTR_CONDITION_POURING,
]


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the binary sensor platform."""
    LOGGER.debug("Setup new entry: %s", config_entry)
    async_add_entities([CheckWeatherSensor(config_entry)])


class CheckWeatherSensor(BinarySensorEntity):
    """Implementation of binary sensor."""

    def __init__(
        self,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        self.entity_description = BinarySensorEntityDescription(
            key=DOMAIN,
            name=NAME,
            icon=ICON_OFF,
            translation_key=DOMAIN,
        )
        self._config_entry = config_entry

        self._attr_is_on = None

        self._attr_condition = None
        self._attr_precipitation = None
        self._attr_strong_wind = None
        self._attr_cold_temperature = None
        self._attr_hot_temperature = None
        self._attr_time = None

        self._attr_unique_id = f"{config_entry.entry_id}_{config_entry.domain}"

        LOGGER.debug("Initiated with entry options: %s", self._config_entry.options)

    @property
    def is_on(self) -> bool:
        """Report if the binary sensor is on."""
        return self._attr_is_on

    @property
    def available(self) -> bool:
        """Check if entity is available."""
        return self._attr_is_on is not None

    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend, if any."""
        return ICON_ON if self.is_on else ICON_OFF

    @property
    def extra_state_attributes(self) -> dict:
        """Return the extra state attributes."""
        return {
            ATTR_CONDITION: self._attr_condition,
            ATTR_PRECIPITATION: self._attr_precipitation,
            ATTR_STRONG_WIND: self._attr_strong_wind,
            ATTR_BAD_WEATHER_TIME: self._attr_time,
            ATTR_COLD_TEMPERATURE: self._attr_cold_temperature,
            ATTR_HOT_TEMPERATURE: self._attr_hot_temperature,
        }

    def get_config_option(self, key: str, default: Any = None) -> any:
        """Get a value from the config entry or default."""
        return self._config_entry.options.get(
            key,
            self._config_entry.data.get(key, default),
        )

    async def call_forecast_service(self, weather_entity: str) -> list:
        """Get the forecast for the weather entity."""
        service_data = {
            "entity_id": weather_entity,
            "type": "hourly",
        }
        entity_forecasts = await self.hass.services.async_call(
            WEATHER_DOMAIN,
            SERVICE_GET_FORECASTS,
            service_data,
            blocking=True,
            return_response=True,
        )
        return entity_forecasts.get(weather_entity, {}).get("forecast")

    async def get_weather_forecast(self, weather_entity: str) -> list:
        """Get the forecast for the weather entity."""
        weather_data = self.hass.states.get(weather_entity)

        LOGGER.debug("Weather data: %s", weather_data)

        if weather_data is None:
            self._attr_is_on = None
            msg = f"Weather entity {weather_entity} not found"
            raise HomeAssistantError(msg)

        forecasts = await self.call_forecast_service(weather_entity)

        if forecasts is None:
            msg = f"Weather forecast is not available for {weather_entity}"
            raise HomeAssistantError(msg)

        return forecasts

    def get_next_n_hours_forecast(self, forecasts: list, hours_to_check: int) -> list:
        """Filter forecasts for the next N hours."""
        end_time = dt_util.now() + dt.timedelta(hours=hours_to_check)
        return [
            entry
            for entry in forecasts
            if dt_util.parse_datetime(entry.get(ATTR_FORECAST_TIME)) < end_time
        ]

    async def async_update(self) -> None:
        """Update the state."""
        weather_entity = self.get_config_option(CONF_WEATHER, DEFAULT_WEATHER)
        hours_to_check = self.get_config_option(CONF_HOURS, DEFAULT_HOURS)
        prec_threshold = self.get_config_option(
            CONF_PREC_THRESHOLD,
            DEFAULT_PREC_THRESHOLD,
        )
        wind_threshold = self.get_config_option(
            CONF_WIND_THRESHOLD,
            DEFAULT_WIND_THRESHOLD,
        )
        min_temp = self.get_config_option(
            CONF_MIN_TEMP,
            DEFAULT_MIN_TEMP,
        )
        max_temp = self.get_config_option(
            CONF_MAX_TEMP,
            DEFAULT_MAX_TEMP,
        )

        forecasts = await self.get_weather_forecast(weather_entity)

        LOGGER.debug("Forecasts: %s", forecasts)
        # Check if any of the forecasts match the conditions
        is_on = True
        bad_condition = None
        precipitation = False
        strong_wind = False
        cold_temperature = False
        hot_temperature = False
        bad_weather_time = None

        for forecast in self.get_next_n_hours_forecast(forecasts, hours_to_check):
            LOGGER.debug("Forecast: %s", forecast)

            if forecast.get(ATTR_FORECAST_CONDITION) in BAD_CONDITIONS:
                bad_condition = forecast.get(ATTR_FORECAST_CONDITION)
            if forecast.get(ATTR_FORECAST_PRECIPITATION) > prec_threshold:
                precipitation = True
            if forecast.get(ATTR_FORECAST_WIND_SPEED) > wind_threshold:
                strong_wind = True
            if forecast.get(ATTR_FORECAST_TEMP) < min_temp:
                cold_temperature = True
            if forecast.get(ATTR_FORECAST_TEMP) > max_temp:
                hot_temperature = True

            if (
                bad_condition
                or precipitation
                or strong_wind
                or cold_temperature
                or hot_temperature
            ):
                is_on = False
                bad_weather_time = forecast.get(ATTR_FORECAST_TIME)
                LOGGER.debug("Bad conditions found at %s", bad_weather_time)
                LOGGER.debug("Bad condition: %s", bad_condition)
                LOGGER.debug("Precipitation: %s", precipitation)
                LOGGER.debug("Strong wind: %s", strong_wind)
                LOGGER.debug("Cold temperature: %s", cold_temperature)
                LOGGER.debug("Hot temperature: %s", hot_temperature)
                break

        self._attr_is_on = is_on
        self._attr_condition = bad_condition or forecasts[0].get(
            ATTR_FORECAST_CONDITION,
        )
        self._attr_precipitation = precipitation
        self._attr_strong_wind = strong_wind
        self._attr_cold_temperature = cold_temperature
        self._attr_hot_temperature = hot_temperature
        self._attr_time = bad_weather_time
