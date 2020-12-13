"""Summary
"""
from datetime import datetime
from typing import Optional, Union

from .base import Stub
from .misc import cast


class State(Stub):
    __key = "drive_state"

    async def refresh(self):
        return await self._vehicle.get_drive_state()

    @property
    def gps_last_update(self) -> datetime:
        """Last update from the grp as datetime"""
        value = self._vehicle._data[self.__key]["gps_as_of"]
        return datetime.utcfromtimestamp(value / 1000)

    @property
    def heading(self) -> int:
        """Heading of the car."""
        return self._vehicle._data[self.__key]["heading"]

    @property
    def latitude(self) -> float:
        """Latitude of the car"""
        return self._vehicle._data[self.__key]["latitude"]

    @property
    def longitude(self) -> float:
        """Latitude of the car"""
        return self._vehicle._data[self.__key]["longitude"]

    @property
    def native_location_supported(self) -> bool:
        return cast(self._vehicle._data[self.__key]["native_location_supported"])

    @property
    def native_latitude(self) -> float:
        """Latitude of the car"""
        return self._vehicle._data[self.__key]["native_latitude"]

    @property
    def native_longitude(self) -> float:
        """Latitude of the car"""
        return self._vehicle._data[self.__key]["native_longitude"]

    @property
    def native_type(self) -> str:
        return self._vehicle._data[self.__key]["native_type"]

    @property
    def power(self):
        """Power usage right know. in wpm or wmk"""
        return self._vehicle._data[self.__key]["power"]

    @property
    def shift_state(self) -> Optional[Union[str, None]]:
        """None, P, D, R, or N"""
        return self._vehicle._data[self.__key]["shift_state"]

    @property
    def speed(self) -> Optional[Union[None, int, float]]:
        """Speed in unit format of the cars
           #TODO check this.

        """
        return self._vehicle._data[self.__key]["speed"]

    @property
    def last_update(self) -> datetime:
        value = self._vehicle._data[self.__key]["timestamp"]
        return datetime.utcfromtimestamp(value / 1000)
