from __future__ import annotations

import asyncio
import logging
from typing import Any

import aiohttp
from aiohttp.client import ClientSession
from aiohttp.typedefs import StrOrURL
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store

from .const import (
    CONF_PROXY,
    CONF_PROXY_PASSWORD,
    CONF_PROXY_USERNAME,
    HACS_DOMAIN,
    PLATFORMS,
    STORAGE_KEY,
    STORAGE_VERSION,
)

_LOGGER = logging.getLogger(__name__)


class Proxy:
    def __init__(self, origin, proxy=None, username=None, password=None):
        self._origin = origin
        self._proxy_info = proxy
        self._proxy_auth = aiohttp.BasicAuth(username, password) if username else None

    def _inject(self, kwargs):
        _LOGGER.debug("Proxying request via %s", self._proxy_info)
        injected = {**kwargs, "proxy": self._proxy_info}
        if self._proxy_auth is not None:
            injected["proxy_auth"] = self._proxy_auth
        return injected

    async def request(self, method: str, url: StrOrURL, **kwargs: Any):
        return await self._origin.request(method, url, **self._inject(kwargs))

    async def get(self, url: StrOrURL, **kwargs: Any):
        return await self._origin.get(url, **self._inject(kwargs))

    async def post(self, url: StrOrURL, **kwargs: Any):
        return await self._origin.post(url, **self._inject(kwargs))

    async def put(self, url: StrOrURL, **kwargs: Any):
        return await self._origin.put(url, **self._inject(kwargs))

    async def patch(self, url: StrOrURL, **kwargs: Any):
        return await self._origin.patch(url, **self._inject(kwargs))

    async def delete(self, url: StrOrURL, **kwargs: Any):
        return await self._origin.delete(url, **self._inject(kwargs))

    async def head(self, url: StrOrURL, **kwargs: Any):
        return await self._origin.head(url, **self._inject(kwargs))

    async def options(self, url: StrOrURL, **kwargs: Any):
        return await self._origin.options(url, **self._inject(kwargs))

    def __getattr__(self, name):
        return getattr(self._origin, name)


async def async_inject_proxy(hass: HomeAssistant, config_entry: ConfigEntry) -> None:
    hacs = hass.data.get(HACS_DOMAIN)
    if hacs is None:
        return

    session = hacs.session
    if isinstance(session, Proxy):
        return

    if not isinstance(session, ClientSession):
        return

    config = {**config_entry.data, **config_entry.options}
    proxy = Proxy(
        session,
        proxy=config.get(CONF_PROXY),
        username=config.get(CONF_PROXY_USERNAME) or None,
        password=config.get(CONF_PROXY_PASSWORD) or None,
    )
    hacs.session = proxy
    hacs.github._session = proxy
    hacs.githubapi._session = proxy


async def async_eject_proxy(hass: HomeAssistant) -> None:
    hacs = hass.data.get(HACS_DOMAIN)
    if hacs is None:
        return

    session = hacs.session
    if not isinstance(session, Proxy):
        return

    origin = session._origin
    hacs.session = origin
    hacs.github._session = origin
    hacs.githubapi._session = origin


async def async_initialize_integration(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
) -> bool:
    store = Store(hass, STORAGE_VERSION, STORAGE_KEY)
    data = await store.async_load()
    enabled = data.get("enabled", True) if data else True

    if enabled:
        await async_inject_proxy(hass, config_entry)

    return True


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    config_entry.add_update_listener(async_reload_entry)
    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)
    return await async_initialize_integration(hass=hass, config_entry=config_entry)


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    await hass.config_entries.async_unload_platforms(config_entry, PLATFORMS)
    await async_eject_proxy(hass)
    return True


async def async_reload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> None:
    await async_unload_entry(hass, config_entry)
    await asyncio.sleep(1)
    await async_setup_entry(hass, config_entry)
