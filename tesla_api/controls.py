from functools import partialmethod

STATE_VENT = 'vent'
STATE_CLOSE = 'close'


class Controls:
    def __init__(self, vehicle):
        self._vehicle = vehicle
        self._api_client = vehicle._api_client

    async def _set_sunroof_state(self, state):
        return await self._vehicle._command('sun_roof_control', {'state': state})
    vent_sunroof = partialmethod(_set_sunroof_state, STATE_VENT)
    close_sunroof = partialmethod(_set_sunroof_state, STATE_CLOSE)

    async def flash_lights(self):
        return await self._vehicle._command('flash_lights')

    async def honk_horn(self):
        return await self._vehicle._command('honk_horn')

    async def open_charge_port(self):
        return await self._vehicle._command('charge_port_door_open')

    async def door_lock(self):
        return await self._vehicle._command('door_lock')

    async def door_unlock(self):
        return await self._vehicle._command('door_unlock')
