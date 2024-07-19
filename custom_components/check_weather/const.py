"""Constants for the Check Weather integration."""

NAME = "Check Weather"
DOMAIN = "check_weather"

# Icons
ICON_ON = "mdi:cloud-check-variant"
ICON_OFF = "mdi:cloud-alert"

# Configuration option
CONF_WEATHER = "weather"
CONF_HOURS = "hours"
CONF_TEMP_THRESHOLD = "temperature_threshold"  # @deprecated
CONF_MIN_TEMP = "min_temperature"
CONF_MAX_TEMP = "max_temperature"
CONF_PREC_THRESHOLD = "precipitation_threshold"
CONF_WIND_THRESHOLD = "wind_threshold"


# Default values
DEFAULT_WEATHER = None
DEFAULT_HOURS = 8
DEFAULT_MIN_TEMP = 10
DEFAULT_MAX_TEMP = 30
DEFAULT_PREC_THRESHOLD = 0.1
DEFAULT_WIND_THRESHOLD = 20

# Attributes
ATTR_CONDITION = "condition"
ATTR_PRECIPIATION = "precipitation"
ATTR_STRONG_WIND = "strong_wind"
ATTR_BAD_WEATHER_TIME = "bad_weather_time"
ATTR_COLD_TEMPERATURE = "cold_temperature"
ATTR_HOT_TEMPERATURE = "hot_temperature"
