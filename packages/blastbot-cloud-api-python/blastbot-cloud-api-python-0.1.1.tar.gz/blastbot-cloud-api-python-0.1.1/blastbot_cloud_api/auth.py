from aiohttp import ClientSession, ClientResponse
import time


class Auth:
    """Class to make authenticated requests."""

    def __init__(self, host: str, access_token: str = ""):
        """Initialize the auth."""
        self.host = host
        self.session = ClientSession()
        self.access_token = access_token
        self.access_token_expires = 0
        self.refresh_token = ""
        self.refresh_token_expires = 0

    async def close(self):
        """Close the http session."""
        await self.session.close()

    async def login(self, email: str, password: str) -> bool:
        body = {
            "email": email,
            "password": password
        }
        response = await self.session.request("POST", f"{self.host}/auth/login", json=body)

        if response.status != 200:
            return False

        body = await response.json()

        self.access_token = body["token"]
        self.access_token_expires = body["expires"]
        self.refresh_token = body["refresh_token"]["token"]
        self.refresh_token_expires = body["refresh_token"]["expires"]

        return True

    async def refresh(self) -> bool:
        """Refresh token"""
        headers = {}
        headers["Authorization"] = f'Bearer {self.refresh_token}'
        response = await self.session.request("POST", f"{self.host}/auth/refresh", headers=headers)

        if response.status != 200:
            return False

        body = await response.json()

        self.access_token = body["token"]
        self.access_token_expires = body["expires"]
        self.refresh_token = body["refresh_token"]["token"]
        self.refresh_token_expires = body["refresh_token"]["expires"]

        return True

    def is_token_expired(self) -> bool:
        """Check if the token is expired"""
        expires = self.access_token_expires/1000
        now = time.time()
        return now >= expires

    async def request(self, method: str, path: str, **kwargs) -> ClientResponse:
        """Make a request."""

        if self.is_token_expired():
            await self.refresh()

        headers = kwargs.get("headers")

        if headers is None:
            headers = {}
        else:
            headers = dict(headers)

        headers["Authorization"] = f'Bearer {self.access_token}'

        return await self.session.request(
            method, f"{self.host}/{path}", **kwargs, headers=headers,
        )
