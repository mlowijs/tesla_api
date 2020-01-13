from datetime import datetime, timedelta
import requests

from .vehicle import Vehicle
from .energy import Energy

TESLA_API_BASE_URL = 'https://owner-api.teslamotors.com/'
TOKEN_URL = TESLA_API_BASE_URL + 'oauth/token'
API_URL = TESLA_API_BASE_URL + 'api/1'

OAUTH_CLIENT_ID = '81527cff06843c8634fdc09e8ac0abefb46ac849f38fe1e431c2ef2106796384'
OAUTH_CLIENT_SECRET = 'c7257eb71a564034f9419ee651c7d0e5f7aa6bfbd18bafb5c5c033b093bb2fa3'

class TeslaApiClient:
    def __init__(self, email, password):
        self._email = email
        self._password = password
        self._token = None

    def _get_new_token(self):
        request_data = {
            'grant_type': 'password',
            'client_id': OAUTH_CLIENT_ID,
            'client_secret': OAUTH_CLIENT_SECRET,
            'email': self._email,
            'password': self._password
        }

        response = requests.post(TOKEN_URL, data=request_data)
        response_json = response.json()

        if response.status_code == 401:
            raise AuthenticationError(response_json)

        return response_json

    def _refresh_token(self, refresh_token):
        request_data = {
            'grant_type': 'refresh_token',
            'client_id': OAUTH_CLIENT_ID,
            'client_secret': OAUTH_CLIENT_SECRET,
            'refresh_token': refresh_token,
        }

        response = requests.post(TOKEN_URL, data=request_data)
        response_json = response.json()

        if response.status_code == 401:
            raise AuthenticationError(response_json)

        return response_json

    def authenticate(self):
        if not self._token:
            self._token = self._get_new_token()

        expiry_time = timedelta(seconds=self._token['expires_in'])
        expiration_date = datetime.fromtimestamp(self._token['created_at']) + expiry_time

        if datetime.utcnow() >= expiration_date:
            self._token = self._refresh_token(self._token['refresh_token'])

    def _get_headers(self):
        return {
            'Authorization': 'Bearer {}'.format(self._token["access_token"])
        }

    def get(self, endpoint):
        self.authenticate()

        response = requests.get('{}/{}'.format(API_URL, endpoint), headers=self._get_headers())
        response_json = response.json()

        if 'error' in response_json:
            raise ApiError(response_json['error'])

        return response_json['response']

    def post(self, endpoint, data = {}):
        self.authenticate()

        response = requests.post('{}/{}'.format(API_URL, endpoint), headers=self._get_headers(), json=data)
        response_json = response.json()

        if 'error' in response_json:
            raise ApiError(response_json['error'])

        return response_json['response']

    def list_vehicles(self):
        return [Vehicle(self, vehicle) for vehicle in self.get('vehicles')]

    def list_energy_sites(self):
        return [Energy(self, products['energy_site_id']) for products in self.get('products')]

class AuthenticationError(Exception):
    def __init__(self, error):
        super().__init__('Authentication to the Tesla API failed: {}'.format(error))

class ApiError(Exception):
    def __init__(self, error):
        super().__init__('Tesla API call failed: {}'.format(error))
