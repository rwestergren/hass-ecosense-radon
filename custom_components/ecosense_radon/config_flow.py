"""Config flow for EcoSense Radon integration."""

from __future__ import annotations

import logging
from typing import Any

import requests
import voluptuous as vol

from pycognito.exceptions import WarrantException

from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigFlowResult
from homeassistant.exceptions import HomeAssistantError

from .api import EcoSenseApiClient
from .const import DOMAIN, CONF_UNIT, UNIT_PCIL, UNIT_BQM3

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_PASSWORD): str,
        vol.Required(CONF_UNIT, default=UNIT_PCIL): vol.In(
            {
                UNIT_PCIL: "pCi/L (Picocuries per Liter)",
                UNIT_BQM3: "Bq/m³ (Becquerels per Cubic Meter)",
            }
        ),
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""

    api_client = EcoSenseApiClient(data[CONF_USERNAME], data[CONF_PASSWORD])

    try:
        # The pycognito library uses synchronous HTTP calls, so we run it in an executor.
        await hass.async_add_executor_job(api_client.authenticate)
    except (WarrantException, requests.exceptions.RequestException) as exc:
        raise CannotConnect from exc

    # Return info that can be used to name the config entry.
    return {"title": data[CONF_USERNAME]}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for EcoSense Radon."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )

        errors = {}

        try:
            info = await validate_input(self.hass, user_input)
        except CannotConnect:
            errors["base"] = "cannot_connect"
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            await self.async_set_unique_id(user_input[CONF_USERNAME])
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

    @staticmethod
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Get the options flow for this handler."""
        return OptionsFlow()


class OptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for EcoSense Radon."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        # Get current unit from options, fallback to data, then to default
        current_unit = self.config_entry.options.get(
            CONF_UNIT, self.config_entry.data.get(CONF_UNIT, UNIT_PCIL)
        )

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_UNIT, default=current_unit): vol.In(
                        {
                            UNIT_PCIL: "pCi/L (Picocuries per Liter)",
                            UNIT_BQM3: "Bq/m³ (Becquerels per Cubic Meter)",
                        }
                    ),
                }
            ),
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""
