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

    def __dir__(self):
        """Include _vehicle keys in dir(), which are accessible with __getattr__()."""
        return super().__dir__() | self._vehicle.keys()

    def __getattr__(self, name):
        """Allow attribute access to _vehicle details."""
        try:
            return self._vehicle[name]
        except KeyError:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
