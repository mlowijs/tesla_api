from functools import partialmethod

from .base import Stub
from .misc import cast


class Windows(Stub):

    async def vent(self, lat=0, lon=0):
        """Controls the windows. Will vent all windows simultaneously."""
        return await self._vehicle._command(
            "window_control", data={"command": "vent", "lat": lat, "lon": lon}
        )

    async def close(self, lat: float = 0.0, lon: float = 0.0):
        """Controls the windows. Will close all windows simultaneously."""
        ds = self._vehicle._data["drive_state"]
        lat = lat or ds.get("latitude")
        lon = lon or ds.get("longitude")
        return await self._vehicle._command(
            "window_control", data={"command": "close", "lat": lat, "lon": lon}
        )

    @property
    def front_driver_window_open(self) -> bool:
        return cast(self._vehicle._data["vehicle_state"]["fd_window"])

    @property
    def front_passanger_window_open(self) -> bool:
        return cast(self._vehicle._data["vehicle_state"]["fp_window"])

    @property
    def rear_driver_door_open(self) -> bool:
        return cast(self._vehicle._data["vehicle_state"]["rd_window"])

    @property
    def rear_passenger_door_open(self) ->:
        return cast(self._vehicle._data["vehicle_state"]["rp_window"])
