import asyncio

STATE_VENT = 'vent'
STATE_CLOSE = 'close'

class Controls:
    def __init__(self, api_client, vehicle_id):
        self._api_client = api_client
        self._vehicle_id = vehicle_id

    async def _set_sunroof_state(self, state):
        return await self._api_client.post(
            'vehicles/{}/command/sun_roof_control'.format(self._vehicle_id),
            {'state': state}
        )

    async def vent_sunroof(self):
        return await self._set_sunroof_state(STATE_VENT)

    async def close_sunroof(self):
        return await self._set_sunroof_state(STATE_CLOSE)

    async def flash_lights(self):
        return await self._api_client.post('vehicles/{}/command/flash_lights'.format(self._vehicle_id))

    async def honk_horn(self):
        return await self._api_client.post('vehicles/{}/command/honk_horn'.format(self._vehicle_id))

    async def open_charge_port(self):
        return await self._api_client.post('vehicles/{}/command/charge_port_door_open'.format(self._vehicle_id))
