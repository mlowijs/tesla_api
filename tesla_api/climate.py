from enum import Enum
from functools import partialmethod
from typing import Optional, TYPE_CHECKING, cast

from .datatypes import ClimateStateResponse

if TYPE_CHECKING:
    from .vehicle import Vehicle


class SeatPosition(Enum):
    DRIVER = 0
    PASSENGER = 1
    REAR_LEFT = 2
    REAR_CENTER = 4
    REAR_RIGHT = 5


class Climate:
    def __init__(self, vehicle: "Vehicle"):
        self._vehicle = vehicle
        self._api_client = vehicle._api_client

    async def get_state(self) -> ClimateStateResponse:
        endpoint = "vehicles/{}/data_request/climate_state".format(self._vehicle.id)
        return cast(ClimateStateResponse, await self._api_client.get(endpoint))

    async def start_climate(self) -> bool:
        return cast(bool, await self._vehicle._command("auto_conditioning_start"))

    async def stop_climate(self) -> bool:
        return cast(bool, await self._vehicle._command("auto_conditioning_stop"))

    async def set_temperature(self, driver_temperature: float,  # TODO: Does int work?
                              passenger_temperature: Optional[float] = None) -> bool:
        data = {"driver_temp": driver_temperature,
                "passenger_temp": passenger_temperature or driver_temperature}
        return cast(bool, await self._vehicle._command("set_temps", data))

    async def set_seat_heater(self, temp: int = 0,
                              seat: SeatPosition = SeatPosition.DRIVER) -> bool:
        """Set a seat heater.

        Args:
            temp: The desired level for the heater. (0-3)
            seat: The desired seat to heat.
        """
        if temp < 0 or temp > 3:
            raise ValueError("temp must be in the range 0-3")

        args = {"heater": seat, "level": temp}
        return cast(bool, await self._vehicle._command("remote_seat_heater_request", args))

    async def steering_wheel_heater(self, on: bool) -> bool:
        endpoint = "remote_steering_wheel_heater_request"
        args = {"on": on}
        return cast(bool, await self._vehicle._command(endpoint, args))
    start_steering_wheel_heater = partialmethod(steering_wheel_heater, True)
    stop_steering_wheel_heater = partialmethod(steering_wheel_heater, False)
