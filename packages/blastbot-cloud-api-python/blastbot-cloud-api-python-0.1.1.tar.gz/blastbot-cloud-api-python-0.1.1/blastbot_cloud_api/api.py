from typing import List
import aiohttp

from .auth import Auth
from .models.device import Device, DEVICE_DEFAULT_PARAMS
from .models.control import Control, CONTROL_DEFAULT_PARAMS

API_URL = "https://cloud.blastbot.io/api/v3"


class BlastbotCloudAPI:
    """Class to communicate with the BlastbotCloud API."""

    def __init__(self):
        """Initialize the API and store the auth so we can make requests."""
        auth = Auth(API_URL)
        self.auth = auth

    async def async_close(self):
        await self.auth.close()

    async def async_login(self, email: str, password: str) -> bool:
        return await self.auth.login(email, password)

    async def async_get_devices(self) -> List[Device]:
        resp = await self.auth.request("get", "device", params=DEVICE_DEFAULT_PARAMS)
        resp.raise_for_status()
        return [Device(data, self.auth) for data in await resp.json()]

    async def async_get_device(self, id: int) -> Device:
        resp = await self.auth.request("get", f"device/{id}", params=DEVICE_DEFAULT_PARAMS)
        resp.raise_for_status()
        return Device(await resp.json(), self.auth)

    async def async_get_controls(self, type: str = None) -> List[Control]:
        params = CONTROL_DEFAULT_PARAMS.copy()
        if type is not None:
            params["where"] = '{"type":"' + type + '"}'
        resp = await self.auth.request("get", "control", params=params)
        resp.raise_for_status()
        return [Control(data, self.auth) for data in await resp.json()]

    async def async_get_control(self, id: int) -> Control:
        resp = await self.auth.request("get", f"control/{id}", params=CONTROL_DEFAULT_PARAMS)
        resp.raise_for_status()
        return Control(await resp.json(), self.auth)

    async def async_get_switches(self) -> List[Control]:
        return await self.async_get_controls("switch")

    async def async_get_acs(self) -> List[Control]:
        return await self.async_get_controls("ac")

    async def async_get_irs(self) -> List[Control]:
        return await self.async_get_controls("ir")
