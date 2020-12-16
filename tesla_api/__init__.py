import asyncio
import json
from datetime import datetime, timedelta
from types import TracebackType
from typing import cast, Awaitable, Callable, Coroutine, Dict, List, Literal, Mapping, Optional, Type, TypedDict, TypeVar, Union

import aiohttp

from .datatypes import (BaseResponse, EnergySite, ErrorResponse, ProductsResponse,
                        TokenParams, TokenResponse, VehiclesResponse)
from .energy import Energy
from .exceptions import (ApiError, AuthenticationError, VehicleInServiceError,
                         VehicleUnavailableError)
from .vehicle import Vehicle

__all__ = ('Energy', 'Vehicle', 'TeslaApiClient', 'ApiError', 'AuthenticationError',
           'VehicleInServiceError', 'VehicleUnavailableError')

TESLA_API_BASE_URL = "https://owner-api.teslamotors.com/"
TOKEN_URL = TESLA_API_BASE_URL + "oauth/token"
API_URL = TESLA_API_BASE_URL + "api/1"

OAUTH_CLIENT_ID = "81527cff06843c8634fdc09e8ac0abefb46ac849f38fe1e431c2ef2106796384"
OAUTH_CLIENT_SECRET = "c7257eb71a564034f9419ee651c7d0e5f7aa6bfbd18bafb5c5c033b093bb2fa3"


class AuthHeaders(TypedDict):
    Authorization: str


class _AuthParamsPassword(TypedDict):
    grant_type: Literal["password"]
    email: str
    password: str


class _AuthParamsRefresh(TypedDict):
    grant_type: Literal["refresh_token"]
    refresh_token: str


AuthParams = Union[_AuthParamsPassword, _AuthParamsRefresh]
T = TypeVar("T", bound="TeslaApiClient")

class TeslaApiClient:
    callback_update: Optional[Callable[[Vehicle], Awaitable[None]]] = None  # Called when vehicle's state has been updated.
    callback_wake_up: Optional[Callable[[Vehicle], Awaitable[None]]] = None  # Called when attempting to wake a vehicle.
    timeout = 30  # Default timeout for operations such as Vehicle.wake_up().

    def __init__(self, email: Optional[str] = None, password: Optional[str] = None,
                 token: Optional[str] = None,
                 on_new_token: Optional[Callable[[str], Awaitable[None]]] = None):
        """Creates client from provided credentials.

        If token is not provided, or is no longer valid, then a new token will
        be fetched if email and password are provided.

        If on_new_token is provided, it will be called with the newly created token.
        This should be used to save the token, both after initial login and after an
        automatic token renewal. The token is returned as a string and can be passed
        directly into this constructor.
        """
        assert token is not None or (email is not None and password is not None)
        self._email = email
        self._password = password
        self._token = cast(TokenResponse, json.loads(token)) if token else None
        self._new_token_callback = on_new_token
        self._session = aiohttp.ClientSession()

    async def close(self) -> None:
        await self._session.close()

    async def _get_token(self, data: AuthParams) -> TokenResponse:
        request_data = cast(TokenParams, {
            "client_id": OAUTH_CLIENT_ID,
            "client_secret": OAUTH_CLIENT_SECRET,
            **data
        })

        async with self._session.post(TOKEN_URL, data=request_data) as resp:
            response_json = await cast(Coroutine[None, None, TokenResponse], resp.json())
            if resp.status == 401:
                raise AuthenticationError(response_json)

        # Send token to application via callback.
        if self._new_token_callback:
            asyncio.create_task(self._new_token_callback(json.dumps(response_json)))

        return response_json

    async def _get_new_token(self) -> TokenResponse:
        assert self._email is not None and self._password is not None
        data = {"grant_type": "password", "email": self._email, "password": self._password}
        return await self._get_token(data)

    async def _refresh_token(self, refresh_token: str) -> TokenResponse:
        data = {"grant_type": "refresh_token", "refresh_token": refresh_token}
        return await self._get_token(data)

    async def authenticate(self) -> None:
        if not self._token:
            self._token = await self._get_new_token()

        expiry_time = timedelta(seconds=self._token["expires_in"])
        expiration_date = datetime.fromtimestamp(self._token["created_at"]) + expiry_time

        if datetime.utcnow() >= expiration_date:
            self._token = await self._refresh_token(self._token["refresh_token"])

    def _get_headers(self) -> AuthHeaders:
        assert self._token is not None
        return {
            'Authorization': 'Bearer {}'.format(self._token['access_token'])
        }

    async def get(self, endpoint: str) -> object:
        return await self._send_request("get", endpoint)

    async def post(self, endpoint: str, data: Optional[Mapping[str, object]] = None) -> object:
        return await self._send_request("post", endpoint, data=data)

    async def _send_request(self, method: Literal["get", "post"], endpoint: str, *,
                            data: Optional[Mapping[str, object]] = None) -> object:
        await self.authenticate()
        url = "{}/{}".format(API_URL, endpoint)

        async with self._session.request(method, url, headers=self._get_headers(), json=data) as resp:
            response_json = await cast(Coroutine[None, None, Union[BaseResponse, ErrorResponse]], resp.json())

        if "error" in response_json:
            error_response = cast(ErrorResponse, response_json)
            error = error_response["error"]
            if "vehicle unavailable" in error:
                raise VehicleUnavailableError()
            elif "in service" in error:
                raise VehicleInServiceError()
            raise ApiError(error)

        response_json = cast(BaseResponse, response_json)
        return response_json["response"]

    async def list_vehicles(self) -> List[Vehicle]:
        vehicles = cast(VehiclesResponse, await self.get('vehicles'))
        return [Vehicle(self, v) for v in vehicles]

    async def list_energy_sites(self) -> List[Energy]:
        products = cast(ProductsResponse, await self.get("products"))
        return [Energy(self, cast(EnergySite, p)["energy_site_id"]) for p in products if "energy_site_id" in p]

    async def __aenter__(self: T) -> T:
        return self

    async def __aexit__(self, exc_type: Optional[Type[BaseException]],
                        exc_val: Optional[BaseException], exc_tb: Optional[TracebackType]) -> None:
        await self.close()
