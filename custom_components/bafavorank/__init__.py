""" The bafavorank integration. """
import logging

from homeassistant import config_entries, core

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: core.HomeAssistant, entry: config_entries.ConfigEntry
) -> bool:
    """Set up platform from a ConfigEntry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True


async def async_setup(hass: core.HomeAssistant, config: dict) -> bool:
    """Set up from yaml configuration."""
    hass.data.setdefault(DOMAIN, {})
    return True
