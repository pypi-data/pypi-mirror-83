from isilon.exceptions import TokenRetrieveException


class Credentials:
    def __init__(self, client):
        self._client = client

    async def token(self, headers: dict = {}):
        headers.update(
            {"X-Storage-User": f"{self._client.account}:{self._client.user}"}
        )
        headers.update({"X-Storage-Pass": f"{self._client.password}"})
        async with self._client.http.get(
            f"{self._client.address}/auth/v1.0", headers=headers
        ) as resp:
            try:
                return resp.headers["X-Auth-Token"]
            except Exception:
                raise TokenRetrieveException

    async def x_auth_token(self, headers: dict = {}):
        token = await self.token(headers)
        return {"X-Auth-Token": token}

    def __repr__(self):
        return f"Credentials(account='{self._client.account}', user='{self._client.user}', password='{self._client.password}')"
