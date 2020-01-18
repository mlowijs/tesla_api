import asyncio
from datetime import datetime, timedelta

import aiohttp

from .vehicle import Vehicle
from .energy import Energy

TESLA_API_BASE_URL = 'https://owner-api.teslamotors.com/'
TOKEN_URL = TESLA_API_BASE_URL + 'oauth/token'
API_URL = TESLA_API_BASE_URL + 'api/1'

OAUTH_CLIENT_ID = '81527cff06843c8634fdc09e8ac0abefb46ac849f38fe1e431c2ef2106796384'
OAUTH_CLIENT_SECRET = 'c7257eb71a564034f9419ee651c7d0e5f7aa6bfbd18bafb5c5c033b093bb2fa3'

class TeslaApiClient:
    def __init__(self, email=None, password=None, token=None):
        """Creates client from provided credentials.

        If token is not provided, or is no longer valid, then a new token will
        be fetched if email and password are provided.
        """
        assert token is not None or (email is not None and password is not None)
        self._email = email
        self._password = password
        self.token = token
        self._session = aiohttp.ClientSession()

    async def close(self):
        await self._session.close()

    async def _get_new_token(self):
        request_data = {
            'grant_type': 'password',
            'client_id': OAUTH_CLIENT_ID,
            'client_secret': OAUTH_CLIENT_SECRET,
            'email': self._email,
            'password': self._password
        }

        async with self._session.post(TOKEN_URL, data=request_data) as resp:
            response_json = await resp.json()
            if resp.status == 401:
                raise AuthenticationError(response_json)

        return response_json

    async def _refresh_token(self, refresh_token):
        request_data = {
            'grant_type': 'refresh_token',
            'client_id': OAUTH_CLIENT_ID,
            'client_secret': OAUTH_CLIENT_SECRET,
            'refresh_token': refresh_token,
        }

        async with self._session.post(TOKEN_URL, data=request_data) as resp:
            response_json = await resp.json()
            if resp.status == 401:
                raise AuthenticationError(response_json)

        return response_json

    async def authenticate(self):
        if not self.token:
            self.token = await self._get_new_token()

        expiry_time = timedelta(seconds=self.token['expires_in'])
        expiration_date = datetime.fromtimestamp(self.token['created_at']) + expiry_time

        if datetime.utcnow() >= expiration_date:
            self.token = await self._refresh_token(self.token['refresh_token'])

    def _get_headers(self):
        return {
            'Authorization': 'Bearer {}'.format(self.token['access_token'])
        }

    async def get(self, endpoint):
        await self.authenticate()
        url = '{}/{}'.format(API_URL, endpoint)

        async with self._session.get(url, headers=self._get_headers()) as resp:
            response_json = await resp.json()

        if 'error' in response_json:
            raise ApiError(response_json['error'])

        return response_json['response']

    async def post(self, endpoint, data = {}):
        await self.authenticate()
        url = '{}/{}'.format(API_URL, endpoint)

        async with self._session.post(url, headers=self._get_headers(), json=data) as resp:
            response_json = await resp.json()

        if 'error' in response_json:
            raise ApiError(response_json['error'])

        return response_json['response']

    async def list_vehicles(self, _class=Vehicle):
        return [_class(self, vehicle) for vehicle in await self.get('vehicles')]

    async def list_energy_sites(self, _class=Energy):
        return [_class(self, products['energy_site_id']) for products in await self.get('products')]

class AuthenticationError(Exception):
    def __init__(self, error):
        super().__init__('Authentication to the Tesla API failed: {}'.format(error))

class ApiError(Exception):
    def __init__(self, error):
        super().__init__('Tesla API call failed: {}'.format(error))
