from __future__ import annotations

import logging

import voluptuous as vol
import datetime as dt
import homeassistant.util.dt as dt_util
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.components.binary_sensor import BinarySensorEntity, PLATFORM_SCHEMA
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.weather import (
    DOMAIN as WEATHER_DOMAIN,
    SERVICE_GET_FORECASTS,
    ATTR_FORECAST_TIME,
    ATTR_FORECAST_CONDITION,
    ATTR_FORECAST_TEMP,
    ATTR_FORECAST_PRECIPITATION,
    ATTR_FORECAST_WIND_SPEED,
    ATTR_CONDITION_LIGHTNING,
    ATTR_CONDITION_LIGHTNING_RAINY,
    ATTR_CONDITION_HAIL,
    ATTR_CONDITION_RAINY,
    ATTR_CONDITION_SNOWY,
    ATTR_CONDITION_SNOWY_RAINY,
    ATTR_CONDITION_POURING,
)

from .const import (
    CONF_HOURS,
    CONF_PREC_THRESHOLD,
    CONF_TEMP_THRESHOLD,
    CONF_WEATHER,
    CONF_WIND_THRESHOLD,
    DEFAULT_HOURS,
    DEFAULT_NAME,
    DEFAULT_PREC_THRESHOLD,
    DEFAULT_TEMP_THRESHOLD,
    DEFAULT_WIND_THRESHOLD,
    ICON_ON,
    ICON_OFF
)

LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_WEATHER): cv.entity_domain(WEATHER_DOMAIN),
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
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

BAD_CONDITIONS = [
    ATTR_CONDITION_LIGHTNING,
    ATTR_CONDITION_LIGHTNING_RAINY,
    ATTR_CONDITION_HAIL,
    ATTR_CONDITION_RAINY,
    ATTR_CONDITION_SNOWY,
    ATTR_CONDITION_SNOWY_RAINY,
    ATTR_CONDITION_POURING,
]

async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
):
    LOGGER.info(config)
    async_add_entities(
        [
            BikeDaySensor(
                config.get(CONF_NAME),
                config.get(CONF_WEATHER),
                config.get(CONF_HOURS),
                config.get(CONF_TEMP_THRESHOLD),
                config.get(CONF_PREC_THRESHOLD),
                config.get(CONF_WIND_THRESHOLD),
            )
        ]
    )


class BikeDaySensor(BinarySensorEntity):
    """Implementation of Bike binary sensor."""

    def __init__(
        self,
        friendly_name: str | None,
        weather_entity: str,
        hours: int,
        temp_threshold: float,
        prec_threshold: float,
        wind_threshold: float,
    ) -> None:
        self._attr_name = friendly_name
        self._attr_is_on = None

        self._attr_unique_id = f"{weather_entity}_{hours}_bike_day"

        self._attr_condition = None
        self._attr_precipitation = None
        self._attr_strong_wind = None
        self._attr_cold_temperature = None
        self._attr_time = None

        self._weather_entity = weather_entity
        self._hours = hours
        self._temp_threshold = temp_threshold
        self._prec_threshold = prec_threshold
        self._wind_threshold = wind_threshold

        LOGGER.debug(
            "Initiated with weather_entity: %s, hours: %i, temp_threshold: %.1f, prec_threshold: %.1f, wind_threshold: %.1f",
            weather_entity,
            hours,
            temp_threshold,
            prec_threshold,
            wind_threshold,
        )

    @property
    def is_on(self) -> bool:
        "Report if the binary sensor is on."
        return self._attr_is_on

    @property
    def available(self) -> bool:
        """Check if entity is available."""
        return self._attr_is_on is not None

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        return ICON_ON if self.is_on else ICON_OFF

    @property
    def extra_state_attributes(self) -> dict:
        """Return the extra state attributes."""
        # FIXME: Define the attributes as constants in const.py
        return {
            "condition": self._attr_condition,
            "precipitation": self._attr_precipitation,
            "strong_wind": self._attr_strong_wind,
            "bad_weather_at": self._attr_time,
            "cold_temperature": self._attr_cold_temperature,
        }

    async def async_update(self) -> None:
        """Update the state."""
        weather_data = self.hass.states.get(self._weather_entity)

        LOGGER.debug("Weather data: %s", weather_data)
        LOGGER.debug("Weather forecast: %s", weather_data.attributes.get('forecast'))


        if weather_data is None:
            self._attr_is_on = None
            raise HomeAssistantError(f"Weather entity {self._weather_entity} not found")

        service_data = {
            "entity_id": self._weather_entity,
            "type": "hourly",
        }
        entity_forecasts = await self.hass.services.async_call(
            WEATHER_DOMAIN, 
            SERVICE_GET_FORECASTS, 
            service_data, 
            blocking=True, 
            return_response=True
        )
        forecasts = entity_forecasts.get(self._weather_entity, {}).get('forecast')

        if forecasts is None:
            self._attr_is_on = None
            raise HomeAssistantError(f"Weather forecast is not available for {self._weather_entity}")

        # Filter forecasts for the next N hours
        end_time = dt_util.now() + dt.timedelta(hours=self._hours)
        hours_forecasts = [
            entry for entry in forecasts
            if dt_util.parse_datetime(entry.get(ATTR_FORECAST_TIME)) < end_time
        ]
        
        # Check if any of the forecasts match the conditions
        bike_day = True
        bad_condition = None
        precipitation = False
        strong_wind = False
        cold_temperature = False
        bad_weather_time = None

        for forecast in hours_forecasts:
            LOGGER.debug("Forecast: %s", forecast)
            
            if forecast.get(ATTR_FORECAST_CONDITION) in BAD_CONDITIONS:
                bad_condition = forecast.get(ATTR_FORECAST_CONDITION)
            if forecast.get(ATTR_FORECAST_PRECIPITATION) > self._prec_threshold:
                precipitation = True
            if forecast.get(ATTR_FORECAST_WIND_SPEED) > self._wind_threshold:
                strong_wind = True
            if forecast.get(ATTR_FORECAST_TEMP) < self._temp_threshold:
                cold_temperature = True

            if bad_condition or precipitation or strong_wind or cold_temperature:
                bike_day = False
                bad_weather_time = forecast.get(ATTR_FORECAST_TIME)
                LOGGER.debug("Bad conditions found at %s", bad_weather_time)
                LOGGER.debug("Bad condition: %s", bad_condition)
                LOGGER.debug("Precipitation: %s", precipitation)
                LOGGER.debug("Strong wind: %s", strong_wind)
                LOGGER.debug("Cold temperature: %s", cold_temperature)
                break

        self._attr_is_on = bike_day
        self._attr_condition = bad_condition or self._weather_entity.attributes.get(ATTR_FORECAST_CONDITION)
        self._attr_precipitation = precipitation
        self._attr_strong_wind = strong_wind
        self._attr_cold_temperature = cold_temperature
        self._attr_time = bad_weather_time
