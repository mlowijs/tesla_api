import asyncio
import base64
import json
from datetime import datetime, timedelta

import aiohttp

from .energy import Energy
from .exceptions import ApiError, AuthenticationError, VehicleUnavailableError, JWTDecodeError
from .vehicle import Vehicle

TESLA_API_BASE_URL = "https://owner-api.teslamotors.com/"
V3TOKEN_URL = "https://auth.tesla.com/oauth2/v3/token"
API_URL = TESLA_API_BASE_URL + "api/1"

V3OAUTH_CLIENT_ID = "ownerapi"
OAUTH_CLIENT_SECRET = "c7257eb71a564034f9419ee651c7d0e5f7aa6bfbd18bafb5c5c033b093bb2fa3"


class TeslaApiClient:
    callback_update = None  # Called when vehicle's state has been updated.
    callback_wake_up = None  # Called when attempting to wake a vehicle.
    timeout = 30  # Default timeout for operations such as Vehicle.wake_up().

    def __init__(self, email=None, password=None, code=None, token=None, on_new_token=None, on_new_toke_args=None):
        """Creates client from provided credentials.

        Email and Password logins (with MFA support) require client side javascript
        to generate a one time code which can be used to create oauth tokens.
        For more information see:
        https://tesla-api.timdorr.com/api-basics/authentication#step-2-obtain-an-authorization-code
        and use the 'code' option to use this module.
        This is currently not implemented and raises an exception.

        If token is not provided, or is no longer valid, then a new token will
        be fetched if a code (obtained from the tesla auth webpage) is available.
        code consist of the itself + a code_verifier, e.g
        code = {'code': 'codedata', 'code_verifier': 'verification data'}

        In March 2022 V2 long lived V2 token have finally be retired in favor of
        the all new V3 tokens with extended access tokens being valid now for
        8 hrs. At introduction of V3 they initially have only been valid for
        300 seconds, too short for serious server applications.

        If on_new_token is provided, it will be called with the newly created token.
        This should be used to save the token, both after initial login and after an
        automatic token renewal. The token is returned as a string and can be passed
        directly into this constructor.
        """
        if email or password:
            raise Exception("Email and Password logins currently not supported")
        assert token is not None or code is not None or (email is not None and password is not None)
        self._on_new_toke_args = on_new_toke_args
        self._code = json.loads(code) if code else None
        self._token = json.loads(token) if token else None
        self._new_token_callback = on_new_token
        self._session = aiohttp.ClientSession()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        await self._session.close()

    def decode_jwt_token(self, jwt_token):
        try:
            headers_enc, payload_enc, verify_signature = jwt_token.split('.')
            payload_enc += '=' * (-len(payload_enc) % 4)  # add padding
            payload = json.loads(base64.b64decode(payload_enc).decode("utf-8"))
            return payload
        except:
            raise JWTDecodeError()

    async def _get_token(self, url, data, headers={}):
        request_data = {
            "client_secret": OAUTH_CLIENT_SECRET,
        }
        request_data.update(data)

        async with self._session.post(url, data=request_data, headers=headers) as resp:
            response_json = await resp.json()
            if resp.status == 401:
                raise AuthenticationError(response_json)
        if "error" in response_json:
            raise AuthenticationError(response_json)
        return response_json

    async def _get_new_token_with_userpass(self):
        #TODO ... do some HTML magic here
        raise Exception('username / password token retrival not implemented yet')

    async def _get_new_token_with_code(self):
        request_data = {"grant_type": "authorization_code", "client_id": V3OAUTH_CLIENT_ID,
            "code": self._code["code"], "code_verifier": self._code["code_verifier"],
            "redirect_uri": "https://auth.tesla.com/void/callback",
        }
        return await self._get_token(V3TOKEN_URL, request_data)

    async def _refresh_token(self, refresh_token):
        request_data = {"grant_type": "refresh_token", "refresh_token": refresh_token, "client_id": V3OAUTH_CLIENT_ID, "scope": "openid email offline_access"}
        v3_token_data = await self._get_token(V3TOKEN_URL, request_data)
        return v3_token_data

    async def authenticate(self, force_refresh=False):
        if not self._token:
            if self._code: # First we check of if have a webcode to generate tokens
                self._token = await self._get_new_token_with_code()
            elif self._email: # Otherwise we try the user / password combo
                self._token = await self._get_new_token_with_userpass()
            else:
                raise AuthenticationError('token or code or username/password missing')

        if "expires_at" not in self._token:
            try:
                jwt_data = self.decode_jwt_token(self._token["access_token"])
            except JWTDecodeError:
                self._token["expires_at"] = self._token["created_at"] + self._token["expires_in"]
            else:
                self._token["expires_at"] = jwt_data["exp"]
        expiration_date = datetime.fromtimestamp(self._token["expires_at"])

        if datetime.utcnow() >= expiration_date or force_refresh:
            token_data = await self._refresh_token(self._token["refresh_token"])
            self._token = token_data

            # Send token to application via callback.
            if self._new_token_callback:
                token_jdump = json.dumps(self._token)
                if self._on_new_toke_args:
                    asyncio.create_task(self._new_token_callback(token_jdump, self._on_new_toke_args))
                else:
                    asyncio.create_task(self._new_token_callback(token_jdump))

    def _get_headers(self):
        return {"Authorization": "Bearer {}".format(self._token["access_token"])}

    async def get(self, endpoint, params=None):
        await self.authenticate()
        url = "{}/{}".format(API_URL, endpoint)

        async with self._session.get(url, headers=self._get_headers(), params=params) as resp:
            try:
                response_json = await resp.json()
            except aiohttp.client_exceptions.ContentTypeError as cte:
                raise VehicleUnavailableError()

        if response_json == None:
           raise VehicleUnavailableError()

        if "error" in response_json:
            if "vehicle unavailable" in response_json["error"]:
                raise VehicleUnavailableError()
            raise ApiError(response_json["error"])

        return response_json["response"]

    async def post(self, endpoint, data=None):
        await self.authenticate()
        url = "{}/{}".format(API_URL, endpoint)

        async with self._session.post(url, headers=self._get_headers(), json=data) as resp:
            try:
                response_json = await resp.json()
            except aiohttp.client_exceptions.ContentTypeError as cte:
                raise VehicleUnavailableError()

        if response_json == None:
           raise VehicleUnavailableError()

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
