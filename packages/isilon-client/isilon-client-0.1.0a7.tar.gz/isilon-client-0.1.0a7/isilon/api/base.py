class BaseAPI:
    API_VERSION = "v1"

    def __init__(self, client):
        self._client = client

    async def include_auth_header(self, **kwargs: dict) -> dict:
        token = await self._client.credentials.x_auth_token()
        kwargs.update({"headers": token})
        return kwargs

    @property
    def address(self):
        return self._client.address

    @property
    def http(self):
        return self._client.http

    @property
    def account(self):
        return self._client.account

    def __repr__(self) -> str:
        *_, name = str(self.__class__).split(".")
        return f"{name[:-2]}(api_version='{self.API_VERSION}')"
