


from .base import Stub
from .misc import cast


class Windows(Stub):

    async def vent(self, lat: float = 0, lon: float = 0) -> bool:
        """Ventilate the Windows


        Note:
            The lat and lon values are ignored by the api.

        Args:
            lat (float, optional): latitude
            lon (float, optional): longitude

        Returns:
            bool: Returns True if success
        """
        lat = lat or self._vehicle.status.latitude
        lon = lon or self._vehicle.status.longitude
        return await self._vehicle._command(
            "window_control", data={"command": "vent", "lat": lat, "lon": lon}
        )


    async def close(self, lat: float = 0, lon: float = 0) -> bool:
        """Close the Windows.

        Note:
            Must be near the current location of the car

        Args:
            lat (float, optional): lat must be near the current location of the car.
            lon (float, optional): lon must be near the current location of the car.

        Returns:
            bool: Returns True if success
        """
        lat = lat or self._vehicle.status.latitude
        lon = lon or self._vehicle.status.longitude
        return await self._vehicle._command(
            "window_control", data={"command": "close", "lat": lat, "lon": lon}
        )

    @property
    def driver_window_open(self) -> bool:
        """Driver window open

        Returns:
            bool: True if the window is open, False it not
        """
        return cast(self._vehicle._data["vehicle_state"]["fd_window"])

    @property
    def passenger_window_open(self) -> bool:
        """Passenger window open

        Returns:
            bool: True if the window is open, False it not
        """
        return cast(self._vehicle._data["vehicle_state"]["fp_window"])

    @property
    def rear_driver_window_open(self) -> bool:
        """Rear driver window open

        Returns:
            bool: True if the window is open, False it not
        """
        return cast(self._vehicle._data["vehicle_state"]["rd_window"])

    @property
    def rear_passenger_window_open(self) -> bool:
        """Rear passenger window open

        Returns:
            bool: True if the window is open, False it not
        """
        return cast(self._vehicle._data["vehicle_state"]["rp_window"])
