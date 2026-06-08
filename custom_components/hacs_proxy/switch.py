from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.storage import Store

from . import Proxy, async_eject_proxy, async_inject_proxy
from .const import DOMAIN, HACS_DOMAIN, STORAGE_KEY, STORAGE_VERSION


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    async_add_entities([ProxySwitch(config_entry)])


class ProxySwitch(SwitchEntity):
    _attr_unique_id = f"{DOMAIN}_proxy_switch"
    _attr_has_entity_name = True
    _attr_translation_key = "proxy_switch"

    def __init__(self, config_entry: ConfigEntry) -> None:
        self._config_entry = config_entry

    @property
    def is_on(self) -> bool:
        hacs = self.hass.data.get(HACS_DOMAIN)
        return hacs is not None and isinstance(hacs.session, Proxy)

    async def async_turn_on(self, **kwargs) -> None:
        await async_inject_proxy(self.hass, self._config_entry)
        store = Store(self.hass, STORAGE_VERSION, STORAGE_KEY)
        await store.async_save({"enabled": True})
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs) -> None:
        await async_eject_proxy(self.hass)
        store = Store(self.hass, STORAGE_VERSION, STORAGE_KEY)
        await store.async_save({"enabled": False})
        self.async_write_ha_state()
