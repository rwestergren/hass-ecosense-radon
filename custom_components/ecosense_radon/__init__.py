"""The EcoSense Radon integration."""

from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform, CONF_USERNAME, CONF_PASSWORD
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .api import EcoSenseApiClient
from .const import DOMAIN, UPDATE_INTERVAL, CONF_UNIT, UNIT_PCIL, UNIT_BQM3

_LOGGER = logging.getLogger(__name__)

# List of platforms to support.
PLATFORMS: list[Platform] = [Platform.SENSOR]

# Maps legacy integer unit values to the current string values.
_LEGACY_UNIT_MAP = {0: UNIT_PCIL, 1: UNIT_BQM3}


async def async_migrate_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Migrate old config entries to the new format."""
    _LOGGER.debug("Migrating EcoSense Radon entry from version %s", entry.version)

    if entry.version == 1:

        def _migrate_unit(source: dict) -> dict:
            """Return a copy of source with the unit value migrated to a string."""
            updated = dict(source)
            if CONF_UNIT in updated:
                updated[CONF_UNIT] = _LEGACY_UNIT_MAP.get(
                    updated[CONF_UNIT], updated[CONF_UNIT]
                )
            return updated

        hass.config_entries.async_update_entry(
            entry,
            data=_migrate_unit(entry.data),
            options=_migrate_unit(entry.options),
            version=2,
        )

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up EcoSense Radon from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    api_client = EcoSenseApiClient(
        username=entry.data[CONF_USERNAME], password=entry.data[CONF_PASSWORD]
    )

    async def async_update_data():
        """Fetch data from API endpoint."""
        return await hass.async_add_executor_job(api_client.get_devices)

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="ecosense_radon_sensor",
        update_method=async_update_data,
        update_interval=timedelta(minutes=UPDATE_INTERVAL),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Reload the entry when its options change (e.g. the unit selection) so
    # changes take effect immediately instead of requiring a restart.
    entry.async_on_unload(entry.add_update_listener(_async_update_listener))

    return True


async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update by reloading the config entry."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
