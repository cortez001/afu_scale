"""AFU 体脂秤集成入口"""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ADDRESS, Platform
from homeassistant.core import HomeAssistant

from .const import CONF_AGE, CONF_HEIGHT_CM, CONF_SEX, DOMAIN
from .coordinator import AfuScaleCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.BINARY_SENSOR, Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    address = entry.data[CONF_ADDRESS].upper()
    coordinator = AfuScaleCoordinator(
        hass,
        address,
        entry.data[CONF_HEIGHT_CM],
        entry.data[CONF_SEX],
        entry.data[CONF_AGE],
    )
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    coordinator.start()
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    coordinator = hass.data[DOMAIN].pop(entry.entry_id)
    await coordinator.stop()
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
