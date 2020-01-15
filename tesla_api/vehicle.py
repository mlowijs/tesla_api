import asyncio

from .charge import Charge
from .climate import Climate
from .controls import Controls

class Vehicle:
    def __init__(self, api_client, vehicle):
        self._api_client = api_client
        self._vehicle = vehicle

        self.charge = Charge(self._api_client, vehicle['id'])
        self.climate = Climate(self._api_client, vehicle['id'])
        self.controls = Controls(self._api_client, vehicle['id'])

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
