from typing import List
from ..auth import Auth

CONTROL_DEFAULT_PARAMS = {
    "include": '[{"Device":["Device.bridge"]},"IRButton","ACSettings","DBControl","Switch","User.owner",{"Control.sharedControl":[{"Device":["Device.bridge"]},"IRButton","ACSettings","DBControl","Switch"]}]'
}


class Control:
    """Class that represents a Control object in the Blastbot Cloud API."""

    def __init__(self, raw_data: dict, auth: Auth):
        self.raw_data = raw_data
        self.auth = auth
        self.temperature = None

    @property
    def id(self) -> int:
        return self.raw_data["id"]

    @property
    def deviceId(self) -> int:
        return self.raw_data["deviceId"]

    @property
    def userId(self) -> int:
        return self.raw_data["userId"]

    @property
    def ownerId(self) -> int:
        return self.raw_data["ownerId"]

    @property
    def originId(self) -> int:
        return self.raw_data["originId"]

    @property
    def sharedControlId(self) -> int:
        return self.raw_data["sharedControlId"]

    @property
    def name(self) -> str:
        return self.raw_data["name"]

    @property
    def type(self) -> str:
        return self.raw_data["type"]

    @property
    def acSettings(self) -> dict:
        return self.raw_data["acSettings"]

    @acSettings.setter
    def acSettings(self, value):
        self.raw_data["acSettings"] = value

    @property
    def buttons(self) -> List[dict]:
        return self.raw_data["buttons"]

    @property
    def device(self) -> dict:
        return self.raw_data["device"]

    @property
    def icon(self) -> str:
        return self.raw_data["icon"]

    @property
    def order(self) -> int:
        return self.raw_data["order"]

    @property
    def origin(self) -> dict:
        return self.raw_data["origin"]

    @property
    def owner(self) -> dict:
        return self.raw_data["owner"]

    @property
    def sharedControl(self) -> dict:
        return self.raw_data["sharedControl"]

    @property
    def switches(self) -> List[dict]:
        return self.raw_data["switches"]

    def switch_state(self) -> bool:
        try:
            return self.switches[0]["state"]
        except:
            return False

    async def async_control_button(self, button_id: int):
        resp = await self.auth.request(
            "get", f"irbutton/{button_id}/execute"
        )
        resp.raise_for_status()

    async def async_control_switch(self, is_on: bool):
        switchId = self.switches[0]["id"]
        command = "on" if is_on else "off"
        resp = await self.auth.request(
            "post", f"switch/{switchId}/execute", json={"command": command}
        )
        resp.raise_for_status()
        self.switches[0] = await resp.json()

    # state: "on" or "off"
    # temperature: number of ºC in string
    # fan: one of "auto", "low", "medium" or "high"
    async def async_control_ac(self,
                               state: str = None,
                               temperature: str = None,
                               fan: str = None):
        acSettingsId = self.acSettings["id"]
        current = self.acSettings
        currentState = current["state"] if current["state"] is not None else "off"
        currentTemp = current["temperature"] if current["temperature"] is not None else "25"
        currentFan = current["fan"] if current["fan"] is not None else "auto"

        command = state if state is not None and currentState != "on" else "set"
        temperature = temperature if temperature is not None else currentTemp
        fan = fan if fan is not None else currentFan
        body = {
            "command": command,
            "options": {
                "temperature": temperature,
                "fan": fan
            }
        }
        resp = await self.auth.request(
            "post", f"acsettings/{acSettingsId}/execute", json=body
        )
        resp.raise_for_status()
        self.acSettings = await resp.json()

    async def async_update(self):
        resp = await self.auth.request("get", f"control/{str(self.id)}", params=CONTROL_DEFAULT_PARAMS)
        resp.raise_for_status()
        self.raw_data = await resp.json()

        if self.type == "ac":
            # Get temp from device
            params = {
                "limit": "1",
                "where": '{"deviceId":' + str(self.deviceId) + '}',
                "order": '[["id", "DESC"]]'
            }
            resp = await self.auth.request("get", "templog", params=params)
            resp.raise_for_status()
            data = await resp.json()
            if len(data) > 0:
                self.temperature = data[0]["temperature"]
