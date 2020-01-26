import asyncio

from .charge import Charge
from .climate import Climate
from .controls import Controls
from .exceptions import ApiError

class Vehicle:
    def __init__(self, api_client, vehicle):
        self._api_client = api_client
        self._vehicle = vehicle

        self.charge = Charge(self)
        self.climate = Climate(self)
        self.controls = Controls(self)

    async def _command(self, command_endpoint, data=None):
        """Handles vehicle commands with the common reason/result response.

        Args:
            command_endpoint: The final part of the endpoint (after /command/).
            data: Optional JSON data to send with the request.

        Raises:
            ApiError on unsuccessful response.
        """
        endpoint = 'vehicles/{}/command/{}'.format(self.id, command_endpoint)
        res = await self._api_client.post(endpoint, data)
        if res.get('result') is not True:
            raise ApiError(res.get('reason', ''))

    async def is_mobile_access_enabled(self):
        return await self._api_client.get('vehicles/{}/mobile_enabled'.format(self.id))

    async def get_data(self):
        return await self._api_client.get('vehicles/{}/vehicle_data'.format(self.id))

    async def get_state(self):
        return await self._api_client.get('vehicles/{}/data_request/vehicle_state'.format(self.id))

    async def get_drive_state(self):
        return await self._api_client.get('vehicles/{}/data_request/drive_state'.format(self.id))

    async def get_gui_settings(self):
        return await self._api_client.get('vehicles/{}/data_request/gui_settings'.format(self.id))

    async def wake_up(self):
        return await self._api_client.post('vehicles/{}/wake_up'.format(self.id))

    async def remote_start(self):
        return await self._command('remote_start_drive')

    @property
    def id(self):
        return self._vehicle['id']

    @property
    def display_name(self):
        return self._vehicle['display_name']

    @property
    def vin(self):
        return self._vehicle['vin']

    @property
    def state(self):
        return self._vehicle['state']
