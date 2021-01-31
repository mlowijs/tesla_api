import asyncio
import base64
import hashlib
import json
import re
import secrets
from datetime import datetime, timedelta
from urllib.parse import parse_qs, urlparse

import aiohttp

from .energy import Energy
from .exceptions import ApiError, AuthenticationError, VehicleUnavailableError
from .vehicle import Vehicle

TESLA_API_BASE_URL = "https://owner-api.teslamotors.com/"
TOKEN_URL = "https://auth.tesla.com/oauth2/v3/authorize"
API_URL = TESLA_API_BASE_URL + "api/1"

OAUTH_CLIENT_ID = "81527cff06843c8634fdc09e8ac0abefb46ac849f38fe1e431c2ef2106796384"
OAUTH_CLIENT_SECRET = "c7257eb71a564034f9419ee651c7d0e5f7aa6bfbd18bafb5c5c033b093bb2fa3"


class TeslaApiClient:
    callback_update = None  # Called when vehicle's state has been updated.
    callback_wake_up = None  # Called when attempting to wake a vehicle.
    timeout = 30  # Default timeout for operations such as Vehicle.wake_up().

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
        self._email = email
        self._password = password
        self._token = json.loads(token) if token else None
        self._new_token_callback = on_new_token
        self._session = aiohttp.ClientSession()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        await self._session.close()

    async def _get_new_token(self):
        code_verifier = secrets.token_urlsafe(64)
        code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).hexdigest().encode())
        state = secrets.token_urlsafe(16)

        params = {
            "client_id": "ownerapi",
            "code_challenge": code_challenge.decode(),
            "code_challenge_method": "S256",
            "redirect_uri": "https://auth.tesla.com/void/callback",
            "response_type": "code",
            "scope": "openid email offline_access",
            "state": state
        }

        async with self._session.get(TOKEN_URL, params=params) as resp:
            response_page = await resp.text()

        input_fields = (f.group(1) for f in re.finditer(r"<input ([^>]+)>", response_page))
        input_fields = ((re.search(r'name="(.*?)"', f), re.search(r'value="(.*?)"', f))
                        for f in input_fields)
        form_data = {name.group(1): value.group(1) if value else ""
                     for name, value in input_fields}
        form_data["identity"] = self._email
        form_data["credential"] = self._password

        async with self._session.post(TOKEN_URL, data=form_data, params=params, allow_redirects=False) as resp:
            if resp.status == 401:
                raise AuthenticationError("Incorrect login")
            if resp.status == 200:
                page = await resp.text()
                errors = json.loads(re.search(r"var messages = (.*);", page).group(1))
                raise AuthenticationError(errors.get("_", errors))

            redirect_location = resp.headers["Location"]
            args = parse_qs(urlparse(redirect_location).query)
            if args["state"][0] != state:
                raise AuthenticationError("Incorrect state (possible CSRF attack).")

        data = {
            "grant_type": "authorization_code",
            "client_id": "ownerapi",
            "code": args["code"][0],
            "code_verifier": code_verifier,
            "redirect_uri": "https://auth.tesla.com/void/callback"
        }
        async with self._session.post("https://auth.tesla.com/oauth2/v3/token", json=data) as resp:
            bearer_token = await resp.json()

        params = {
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "client_id": OAUTH_CLIENT_ID,
            "client_secret": OAUTH_CLIENT_SECRET
        }
        headers = {"Authorization": "Bearer {}".format(bearer_token["access_token"])}
        async with self._session.post("https://owner-api.teslamotors.com/oauth/token",
                                      headers=headers, params=params) as resp:
            access_token = await resp.json()

        # Replace the broken refresh token with the token from the previous step.
        access_token["refresh_token"] = bearer_token["refresh_token"]

        # Send token to application via callback.
        if self._new_token_callback:
            asyncio.create_task(self._new_token_callback(json.dumps(access_token)))

        return access_token

    async def _refresh_token(self, refresh_token):
        data = {"grant_type": "refresh_token", "refresh_token": refresh_token}
        return await self._get_token(data)

    async def authenticate(self):
        if not self._token:
            self._token = await self._get_new_token()

        expiry_time = timedelta(seconds=self._token["expires_in"])
        expiration_date = datetime.fromtimestamp(self._token["created_at"]) + expiry_time

        if datetime.utcnow() >= expiration_date:
            self._token = await self._refresh_token(self._token["refresh_token"])

    def _get_headers(self):
        return {"Authorization": "Bearer {}".format(self._token["access_token"])}

    async def get(self, endpoint, params=None):
        await self.authenticate()
        url = "{}/{}".format(API_URL, endpoint)

        async with self._session.get(url, headers=self._get_headers(), params=params) as resp:
            response_json = await resp.json()

        if "error" in response_json:
            if "vehicle unavailable" in response_json["error"]:
                raise VehicleUnavailableError()
            raise ApiError(response_json["error"])

        return response_json["response"]

    async def post(self, endpoint, data=None):
        await self.authenticate()
        url = "{}/{}".format(API_URL, endpoint)

        async with self._session.post(url, headers=self._get_headers(), json=data) as resp:
            response_json = await resp.json()

        if "error" in response_json:
            if "vehicle unavailable" in response_json["error"]:
                raise VehicleUnavailableError()
            raise ApiError(response_json["error"])

        return response_json["response"]

    async def list_vehicles(self):
        return [Vehicle(self, vehicle) for vehicle in await self.get("vehicles")]

    async def list_energy_sites(self):
        return [Energy(self, product["energy_site_id"])
                for product in await self.get("products") if "energy_site_id" in product]
