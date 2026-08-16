"""AFU 体脂秤集成配置流"""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_ADDRESS
from homeassistant.core import HomeAssistant, callback

from .const import (
    CONF_AGE,
    CONF_HEIGHT_CM,
    CONF_SEX,
    DEFAULT_AGE,
    DEFAULT_HEIGHT_CM,
    DEFAULT_SEX,
    DOMAIN,
)

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ADDRESS): str,
        vol.Optional(CONF_HEIGHT_CM, default=DEFAULT_HEIGHT_CM): vol.All(
            vol.Coerce(float), vol.Range(min=50, max=250)
        ),
        vol.Optional(CONF_SEX, default=DEFAULT_SEX): vol.In(["male", "female"]),
        vol.Optional(CONF_AGE, default=DEFAULT_AGE): vol.All(
            vol.Coerce(int), vol.Range(min=1, max=120)
        ),
    }
)


class AfuScaleConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """AFU 体脂秤配置流"""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            address = str(user_input[CONF_ADDRESS]).strip().upper()
            if not self._valid_mac(address):
                errors[CONF_ADDRESS] = "invalid_mac"
            else:
                await self.async_set_unique_id(address)
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=f"AFU 体脂秤 {address}",
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=DATA_SCHEMA,
            errors=errors,
        )

    @staticmethod
    def _valid_mac(address: str) -> bool:
        parts = address.split(":")
        return len(address) == 17 and len(parts) == 6 and all(
            len(p) == 2 for p in parts
        )
