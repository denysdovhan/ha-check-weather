"""
Diagnostics support for Check Weather.

See https://developers.home-assistant.io/docs/core/integration_diagnostics
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.helpers import entity_registry as er

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    entity_registry = er.async_get(hass)
    entities = er.async_entries_for_config_entry(entity_registry, entry.entry_id)

    entity_states: dict[str, Any] = {}
    for entity in entities:
        state = hass.states.get(entity.entity_id)
        entity_states[entity.entity_id] = {
            "original_name": entity.original_name,
            "unique_id": entity.unique_id,
            "state": state.state if state else None,
            "attributes": state.attributes if state else None,
        }

    return {
        "entry": {
            "entry_id": entry.entry_id,
            "version": entry.version,
            "minor_version": entry.minor_version,
            "domain": entry.domain,
            "title": entry.title,
            "state": str(entry.state),
            "data": dict(entry.data),
            "options": dict(entry.options),
        },
        "entities": entity_states,
    }
