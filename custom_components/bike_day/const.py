from homeassistant.const import CONF_NAME

NAME = "Bike Day"
DOMAIN = "bike_day"

# Icons
ICON_ON = "mdi:bike-fast"
ICON_OFF = "mdi:bike"

# Configuration option
CONF_NAME = CONF_NAME
CONF_WEATHER = "weather"
CONF_HOURS = "hours"
CONF_TEMP_THRESHOLD = "temperature_threshold"
CONF_PREC_THRESHOLD = "precipitation_threshold"
CONF_WIND_THRESHOLD = "wind_threshold"

# Default values
DEFAULT_NAME = NAME
DEFAULT_WEATHER = None
DEFAULT_HOURS = 8
DEFAULT_TEMP_THRESHOLD = 10
DEFAULT_PREC_THRESHOLD = 0.1
DEFAULT_WIND_THRESHOLD = 20
