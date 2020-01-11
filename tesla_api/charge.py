import asyncio

class Charge:
    def __init__(self, api_client, vehicle_id):
        self._api_client = api_client
        self._vehicle_id = vehicle_id

    async def get_state(self):
        return await self._api_client.get('vehicles/{}/data_request/charge_state'.format(self._vehicle_id))

    async def start_charging(self):
        return await self._api_client.post('vehicles/{}/command/charge_start'.format(self._vehicle_id))

    async def stop_charging(self):
        return await self._api_client.post('vehicles/{}/command/charge_stop'.format(self._vehicle_id))

    async def set_charge_limit(self, percentage):
        percentage = round(percentage)

        if not (50 <= percentage <= 100):
            raise ValueError('Percentage should be between 50 and 100')

        return await self._api_client.post(
            'vehicles/{}/command/set_charge_limit'.format(self._vehicle_id),
            {'percent': percentage}
        )

class ChargeSync(Charge):
    def get_state(self):
        return asyncio.get_event_loop().run_until_complete(super().get_state())

    def start_charging(self):
        return asyncio.get_event_loop().run_until_complete(super().start_charging())

    def stop_charging(self):
        return asyncio.get_event_loop().run_until_complete(super().stop_charging())

    def set_charge_limit(self, percentage):
        return asyncio.get_event_loop().run_until_complete(super().set_charge_limit(percentage))
