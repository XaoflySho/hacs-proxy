from homeassistant import config_entries
from homeassistant.core import callback
import voluptuous as vol

from .const import CONF_ENABLE, CONF_PROXY, DOMAIN


class ProxyFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for HACS."""

    VERSION = 1

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_user(self, user_input):
        """Handle a flow initialized by the user."""
        self._errors = {}
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")
        
        if user_input:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_ENABLE, default=True): bool,
                    vol.Required(CONF_PROXY, ): str,
                }
            ),
            errors=self._errors,
        )


    @staticmethod
    @callback
    def async_get_options_flow(_config_entry):
        return ProxyOptionsFlowHandler()


class ProxyOptionsFlowHandler(config_entries.OptionsFlow):

    async def async_step_init(self, _user_input=None):
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current = {**self.config_entry.data, **self.config_entry.options}
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_ENABLE, default=current.get(CONF_ENABLE, True)): bool,
                    vol.Required(CONF_PROXY, default=current.get(CONF_PROXY, "")): str,
                }
            ),
        )
