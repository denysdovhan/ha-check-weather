"""Init file for the Check Weather integration."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from homeassistant.const import Platform

from .const import CONF_MAX_TEMP, CONF_MIN_TEMP, CONF_TEMP_THRESHOLD, DEFAULT_MAX_TEMP

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant


LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.BINARY_SENSOR]


async def async_migrate_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Migrate old entry."""
    LOGGER.debug(
        "Migrating configuration from version %s.%s",
        config_entry.version,
        config_entry.minor_version,
    )

    version = config_entry.version

    if version == 1:
        LOGGER.debug("Migrating temperature threshold to min/max temperature.")
        data = {**config_entry.data}
        if CONF_TEMP_THRESHOLD in data:
            temp_threshold = data.pop(CONF_TEMP_THRESHOLD)
            data[CONF_MIN_TEMP] = temp_threshold
            data[CONF_MAX_TEMP] = DEFAULT_MAX_TEMP
        hass.config_entries.async_update_entry(config_entry, data=data, version=2)

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up a new entry."""
    LOGGER.info("Setup entry: %s", entry)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Handle removal of an entry."""
    LOGGER.info("Unload entry: %s", entry)
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> None:
    """Reload config entry."""
    LOGGER.info("Reload entry: %s", entry)
    return await hass.config_entries.async_reload(entry.entry_id)
