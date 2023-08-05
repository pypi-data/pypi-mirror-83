from ..auth import Auth

DEVICE_DEFAULT_PARAMS = {
    "include": '["Device"]'
}


class Device:
    """Class that represents a Device object in the Blastbot Cloud API."""

    def __init__(self, raw_data: dict, auth: Auth):
        self.raw_data = raw_data
        self.auth = auth

    @property
    def id(self) -> int:
        return self.raw_data["id"]

    @property
    def address(self) -> int:
        return self.raw_data["address"]

    @property
    def bridge(self) -> dict:
        return self.raw_data["bridge"]

    @property
    def bridgeId(self) -> int:
        return self.raw_data["bridgeId"]

    @property
    def config(self) -> dict:
        return self.raw_data["config"]

    @property
    def connected(self) -> bool:
        return self.raw_data["connected"]

    @property
    def duration(self) -> int:
        return self.raw_data["duration"]

    @property
    def expiredAt(self) -> int:
        return self.raw_data["expiredAt"]

    @property
    def houseId(self) -> int:
        return self.raw_data["houseId"]

    @property
    def lastSeen(self) -> int:
        return self.raw_data["lastSeen"]

    @property
    def loggedAt(self) -> int:
        return self.raw_data["loggedAt"]

    @property
    def mac(self) -> str:
        return self.raw_data["mac"]

    @property
    def state(self) -> str:
        return self.raw_data["state"]

    @property
    def token(self) -> str:
        return self.raw_data["token"]

    @property
    def udid(self) -> str:
        return self.raw_data["udid"]

    @property
    def version(self) -> str:
        return self.raw_data["version"]

    @property
    def userId(self) -> int:
        return self.raw_data["userId"]

    @property
    def name(self) -> str:
        return self.raw_data["name"]

    @property
    def type(self) -> str:
        return self.raw_data["type"]

    async def async_update(self):
        resp = await self.auth.request("get", f"device/{self.id}", params=DEVICE_DEFAULT_PARAMS)
        resp.raise_for_status()
        self.raw_data = await resp.json()
