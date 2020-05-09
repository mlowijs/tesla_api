import asyncio
import json
from datetime import datetime, timedelta

import aiohttp

from .exceptions import ApiError, AuthenticationError, VehicleUnavailableError
from .vehicle import Vehicle
from .energy import Energy

TESLA_API_BASE_URL = 'https://owner-api.teslamotors.com/'
TOKEN_URL = TESLA_API_BASE_URL + 'oauth/token'
API_URL = TESLA_API_BASE_URL + 'api/1'

OAUTH_CLIENT_ID = '81527cff06843c8634fdc09e8ac0abefb46ac849f38fe1e431c2ef2106796384'
OAUTH_CLIENT_SECRET = 'c7257eb71a564034f9419ee651c7d0e5f7aa6bfbd18bafb5c5c033b093bb2fa3'

class TeslaApiClient:
    callback_update = None  # Called when vehicle's state has been updated.
    callback_wake_up = None  # Called when attempting to wake a vehicle.

    def __init__(self, email=None, password=None, token=None, on_new_token=None):
        """Creates client from provided credentials.

        If token is not provided, or is no longer valid, then a new token will
        be fetched if email and password are provided.

        If on_new_token is provided, it will be called with the newly created token.
        This should be used to save the token, both after initial login and after an
        automatic token renewal. The token is returned as a string and can be passed
        directly into this constructor.
        """
        assert token is not None or (email is not None and password is not None)
        assert on_new_token is None or callable(on_new_token)
        self._email = email
        self._password = password
        self._token = json.loads(token) if token else None
        self._new_token_callback = on_new_token
        self._session = aiohttp.ClientSession()

    @property
    def token(self):
        """
        The authentication token in JSON string format

        Contains expiration data and a refresh token, an must be presented in full to the constructor
        as an alternative to email/password authentication
        """
        return json.dumps(self._token)

    async def close(self):
        await self._session.close()

    async def _get_token(self, data):
        request_data = {
            'client_id': OAUTH_CLIENT_ID,
            'client_secret': OAUTH_CLIENT_SECRET
        }
        request_data.update(data)

        async with self._session.post(TOKEN_URL, data=request_data) as resp:
            response_json = await resp.json()
            if resp.status == 401:
                raise AuthenticationError(response_json)

        # Send token to application via callback.
        if self._new_token_callback:
            self._new_token_callback(json.dumps(response_json))

        return response_json

    async def _get_new_token(self):
        return await self._get_token({'grant_type': 'password', 'email': self._email,
                                      'password': self._password})

    async def _refresh_token(self, refresh_token):
        return await self._get_token({'grant_type': 'refresh_token',
                                      'refresh_token': refresh_token})

    async def authenticate(self):
        if not self._token:
            self._token = await self._get_new_token()

        expiry_time = timedelta(seconds=self._token['expires_in'])
        expiration_date = datetime.fromtimestamp(self._token['created_at']) + expiry_time

        if datetime.utcnow() >= expiration_date:
            self._token = await self._refresh_token(self._token['refresh_token'])

    def _get_headers(self):
        return {
            'Authorization': 'Bearer {}'.format(self._token['access_token'])
        }

    async def get(self, endpoint):
        await self.authenticate()
        url = '{}/{}'.format(API_URL, endpoint)

        async with self._session.get(url, headers=self._get_headers()) as resp:
            response_json = await resp.json()

        if 'error' in response_json:
            if 'vehicle unavailable' in response_json['error']:
                raise VehicleUnavailableError()
            raise ApiError(response_json['error'])

        return response_json['response']

    async def post(self, endpoint, data=None):
        await self.authenticate()
        url = '{}/{}'.format(API_URL, endpoint)

        async with self._session.post(url, headers=self._get_headers(), json=data) as resp:
            response_json = await resp.json()

        if 'error' in response_json:
            if 'vehicle unavailable' in response_json['error']:
                raise VehicleUnavailableError()
            raise ApiError(response_json['error'])

        return response_json['response']

    async def list_vehicles(self, _class=Vehicle):
        return [_class(self, vehicle) for product in await self.get('vehicles') if 'vehicle_id' in product]

    async def list_energy_sites(self, _class=Energy):
        return [_class(self, product['energy_site_id']) for product in await self.get('products') if 'energy_site_id' in product]


