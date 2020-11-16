from functools import partialmethod

from .base import Stub
from .misc import cast, mile_to_km


class Doors(Stub):

    async def lock_door(self):
        return await self._vehicle._command("door_lock")

    async def unlock_door(self):
        return await self._vehicle._command("door_unlock")

    @property
    def front_driver_door_open(self):
        return cast(self._vehicle._data["vehicle_state"]["df"])

    @property
    def rear_driver_door_open(self):
        return cast(self._vehicle._data["vehicle_state"]["dr"])

    @property
    def front_passanger_door_open(self):
        return cast(self._vehicle._data["vehicle_state"]["pf"])

    @property
    def rear_passenger_door_open(self):
        return cast(self._vehicle._data["vehicle_state"]["pr"])
