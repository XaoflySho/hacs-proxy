from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

import asyncio
from aiohttp.client import ClientSession
from aiohttp.typedefs import StrOrURL

from .const import CONF_ENABLE, CONF_PROXY, DOMAIN, HACS_DOMAIN

class Proxy:
    def __init__(self, origin, proxy=None):
        self._origin = origin
        self._proxy_info = proxy

    def _inject(self, kwargs):
        return {**kwargs, 'proxy': self._proxy_info}

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

async def async_initialize_integration(
    hass: HomeAssistant,
    config_entry: ConfigEntry | None = None,
) -> bool:
    """Initialize the integration"""
    hacs = hass.data.get(HACS_DOMAIN)
    if hacs is None:
        return False
    
    config = {**config_entry.data, **config_entry.options}
    if not config.get(CONF_ENABLE):
        return True

    session = hacs.session
    if not isinstance(session, ClientSession):
        return True

    proxy = Proxy(session, config.get(CONF_PROXY))
    hacs.session = proxy
    hacs.github._session = proxy
    hacs.githubapi._session = proxy

    return True

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up this integration using UI."""
    config_entry.add_update_listener(async_reload_entry)
    return await async_initialize_integration(hass=hass, config_entry=config_entry)


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    hacs = hass.data.get(HACS_DOMAIN)
    if hacs is None:
        return True

    session = hacs.session
    if not isinstance(session, Proxy):
        return True

    origin = session._origin
    hacs.session = origin
    hacs.github._session = origin
    hacs.githubapi._session = origin

    return True


async def async_reload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> None:
    """Reload the HACS config entry."""
    await async_unload_entry(hass, config_entry)
    await asyncio.sleep(1)
    await async_setup_entry(hass, config_entry)
