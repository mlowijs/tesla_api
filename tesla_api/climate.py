"""Climate"""
from datetime import datetime
from functools import partialmethod
from typing import Optional

from .base import Stub


class Climate(Stub):
    __key = "climate_state"

    async def refresh(self) -> dict:
        return await self._vehicle.get_climate_state()

    async def start_climate(self) -> bool:
        """Start climate"""
        return await self._vehicle._command("auto_conditioning_start")

    async def stop_climate(self) -> bool:
        """Stop climate."""
        return await self._vehicle._command("auto_conditioning_stop")

    async def enable_max_defrost(self, on: bool = True) -> bool:
        """Toggles the climate controls between Max Defrost and the previous setting."""
        return await self._vehicle._command("set_preconditioning_max", data={"on": on})

    disable_max_defrost = partialmethod(enable_max_defrost, on=False)

    async def set_temperature(
        self, driver_temperature: int, passenger_temperature: Optional[int] = None
    ) -> bool:
        """Set temperatur on the driver and/or passenger side."""
        # check what format this is in.
        data = {
            "driver_temp": driver_temperature,
            "passenger_temp": passenger_temperature or driver_temperature,
        }
        return await self._vehicle._command("set_temps", data=data)

    async def set_seat_heater(self, temp: int = 0, seat: int = 0) -> bool:
        """Turn on the seat heater.

        Args:
            temp (int): The desired level for the header 0-3
            seat (int): What seat to enable.

                0 - Driver
                1 - Passenger
                2 - Rear left
                4 - Rear center
                5 - Rear right
        """
        if not (0 <= temp <= 3):
            raise ValueError("Temp must in 0-3")

        if not (0 <= seat <= 5):
            raise ValueError("Seat must in 0-5")

        return await self._vehicle._command(
            "remote_seat_heater_request", {"heater": seat, "level": temp}
        )

    async def steering_wheel_heater(self, on: bool = True) -> bool:
        """"Turn on or off the steering wheel heater"""
        return await self._vehicle._command(
            "remote_steering_wheel_heater_request", {"on": on}
        )

    start_steering_wheel_heater = partialmethod(steering_wheel_heater, True)
    stop_steering_wheel_heater = partialmethod(steering_wheel_heater, False)

    @property
    def battery_heater(self) -> bool:
        """Is the battery heater on."""
        return self._vehicle._data[self.__key]["battery_heater"]

    @property
    def battery_heater_no_power(self) -> bool:
        """If the soc is to low on enable the battery heater."""
        return bool(self._vehicle._data[self.__key]["battery_heater_no_power"])

    @property
    def climate_keeper_mode(self) -> str:
        """Climate keeper mode."""
        return self._vehicle._data[self.__key]["climate_keeper_mode"]

    @property
    def defrost_mode(self) -> int:
        """Defrost mode"""
        return self._vehicle._data[self.__key]["defrost_mode"]

    @property
    def driver_temp_setting(self) -> float:  # should be bool? is this defrost mode?
        return self._vehicle._data[self.__key]["driver_temp_setting"]

    @property
    def fan_status(self) -> int:
        return self._vehicle._data[self.__key]["fan_status"]

    @property
    def inside_temp(self) -> float:
        return self._vehicle._data[self.__key]["inside_temp"]

    @property
    def is_auto_conditioning_on(self) -> bool:
        return self._vehicle._data[self.__key]["is_auto_conditioning_on"]

    @property
    def is_climate_on(self) -> bool:
        return self._vehicle._data[self.__key]["is_climate_on"]

    @property
    def is_front_defroster_on(self) -> bool:
        return self._vehicle._data[self.__key]["is_front_defroster_on"]

    @property
    def is_preconditioning(self) -> bool:
        return self._vehicle._data[self.__key]["is_preconditioning"]

    @property
    def is_rear_defroster_on(self) -> bool:
        return self._vehicle._data[self.__key]["is_rear_defroster_on"]

    @property
    def left_temp_direction(self) -> int:
        return self._vehicle._data[self.__key]["left_temp_direction"]

    @property
    def max_avail_temp(self) -> int:
        """Maximum available temperature."""
        return self._vehicle._data[self.__key]["max_avail_temp"]

    @property
    def min_avail_temp(self) -> int:
        """Minimum available temperature."""
        return self._vehicle._data[self.__key]["min_avail_temp"]

    @property
    def outside_temp(self) -> float:
        """Outside temperature."""
        return self._vehicle._data[self.__key]["outside_temp"]

    @property
    def passenger_temp_setting(self) -> float:
        """Passenger temperature setting"""
        return self._vehicle._data[self.__key]["passenger_temp_setting"]

    @property
    def remote_heater_control_enabled(self) -> bool:
        return self._vehicle._data[self.__key]["remote_heater_control_enabled"]

    @property
    def right_temp_direction(self) -> int:
        return self._vehicle._data[self.__key]["right_temp_direction"]

    @property
    def seat_heater_left(self) -> int:
        # Should this be driver / passanger
        # we can check if the car is right hand drive in the config
        return self._vehicle._data[self.__key]["seat_heater_left"]

    @property
    def seat_heater_rear_center(self) -> int:
        return self._vehicle._data[self.__key]["seat_heater_rear_center"]

    @property
    def seat_heater_rear_left(self) -> int:
        return self._vehicle._data[self.__key]["seat_heater_rear_left"]

    @property
    def seat_heater_rear_right(self) -> int:
        return self._vehicle._data[self.__key]["seat_heater_rear_right"]

    @property
    def seat_heater_right(self) -> int:
        return self._vehicle._data[self.__key]["seat_heater_right"]

    @property
    def side_mirror_heaters(self) -> bool:
        """Side mirror heaters on."""
        return self._vehicle._data[self.__key]["side_mirror_heaters"]

    @property
    def wiper_blade_heater(self) -> bool:
        """Returs True if the wiper blade heater is on."""
        return self._vehicle._data[self.__key]["wiper_blade_heater"]

    @property
    def last_update(self) -> datetime:
        """Last update."""
        value = self._vehicle._data[self.__key]["timestamp"]
        return datetime.utcfromtimestamp(value / 1000)
