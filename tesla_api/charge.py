from datetime import datetime, timedelta
from typing import Optional, Union

from mypy_extensions import TypedDict

from .base import Stub
from .misc import mile_to_km


"""
class ChargeRefreshTypedDict(TypedDict):
    battery_heater_on: bool
    battery_level: int
    battery_range: float
    charge_current_request: int
    charge_current_request_max: int
    charge_enable_request: bool
    charge_energy_added: float
    charge_limit_soc: int
    charge_limit_soc_max: int
    charge_limit_soc_min: int
    charge_limit_soc_std: int
    charge_miles_added_ideal: float
    charge_miles_added_rated: float
    charge_port_cold_weather_mode: bool
    charge_port_door_open: bool
    charge_port_latch: str
    charge_rate: float
    charge_to_max_range: bool
    charger_actual_current: int
    charger_phases: None
    charger_pilot_current: int
    charger_power: int
    charger_voltage: int
    charging_state: str
    conn_charge_cable: str
    est_battery_range: float
    fast_charger_brand: str
    fast_charger_present: bool
    fast_charger_type: str
    ideal_battery_range: float
    managed_charging_active: bool
    managed_charging_start_time: None
    managed_charging_user_canceled: bool
    max_range_charge_counter: int
    minutes_to_full_charge: int
    not_enough_power_to_heat: None
    scheduled_charging_pending: bool
    scheduled_charging_start_time: None
    time_to_full_charge: float
    timestamp: int
    trip_charging: bool
    usable_battery_level: int
    user_charge_enable_request: None
"""

class Charge(Stub):

    async def refresh(self) -> dict: # ChargeRefreshTypedDict
        return await self._vehicle.get_charge_state()

    async def open_charge_port(self) -> bool:
        """Open charge port."""
        return await self._vehicle._command("charge_port_door_open")

    async def close_charge_port(self) -> bool:
        """Close charge port."""
        return await self._vehicle._command("charge_port_door_close")

    async def start_charging(self) -> bool:
        """Start charging."""
        return await self._vehicle._command("charge_start")

    async def stop_charging(self) -> bool:
        """Stop charging."""
        return await self._vehicle._command("charge_stop")

    # Should the set be changed with enable
    async def set_standard_range_limit(self) -> bool:
        return await self._vehicle._command("charge_standard")

    async def set_max_range_limit(self) -> bool:
        return await self._vehicle._command("charge_max_range")

    async def set_charge_limit(self, percentage: int) -> bool:
        """Set charge limit."""
        percentage = round(percentage)

        if not (50 <= percentage <= 100):
            raise ValueError("Percentage should be between 50 and 100")

        return await self._vehicle._command("set_charge_limit", {"percent": percentage})


    @property
    def current_request(self) -> int:
        # Maximum current (Ampere) that can be requested from the charger
        return self._vehicle._data["charge_state"]["charge_current_request"]

    @property
    def current_request_max(self) -> int:
        # Maximum current (Ampere) that can be requested from the charger
        return self._vehicle._data["charge_state"]["charge_current_request_max"]

    @property
    def enable_request(self) -> bool:
        return self._vehicle._data["charge_state"]["charge_enable_request"]

    @property
    def energy_added(self) -> float:
        return self._vehicle._data["charge_state"]["charge_energy_added"]

    @property
    def limit(self) -> int:
        return self._vehicle._data["charge_state"]["charge_limit_soc"]

    @property
    def limit_max(self) -> int:
        return self._vehicle._data["charge_state"]["charge_limit_soc_max"]

    @property
    def limit_min(self) -> int:
        return self._vehicle._data["charge_state"]["charge_limit_soc_min"]

    @property
    def limit_std(self) -> int:
        return self._vehicle._data["charge_state"]["charge_limit_soc_std"]

    @property
    def miles_added_ideal(self) -> float:
        return self._vehicle._data["charge_state"]["charge_miles_added_ideal"]

    @property
    def miles_added_rated(self) -> float:
        """Rated range added in km added into the battery."""
        return self._vehicle._data["charge_state"]["charge_miles_added_rated"]

    @property
    def km_added_ideal(self) -> float:
        """kWh added into the battery."""
        return mile_to_km(self.miles_added_ideal)

    @property
    def km_added_rated(self) -> float:
        """Rated range added in km added into the battery."""
        return mile_to_km(self.miles_added_rated)

    @property
    def port_cold_weather_mode(self) -> bool:
        # is this the charge port heater, if we it should be renamed.
        return self._vehicle._data["charge_state"]["charge_port_cold_weather_mode"]

    @property
    def port_door_open(self) -> bool:
        # is this the charge port heater, if we it should be renamed.
        return self._vehicle._data["charge_state"]["charge_port_door_open"]

    @property
    def port_latch(self) -> bool:
        # this should be bool but i assume mypy uses True
        value = self._vehicle._data["charge_state"]["charge_port_latch"]
        if value and value.lower() == "engaged":
            return True
        else:
            return False

    @property
    def rate(self) -> float:
        """The charge speed in kWh."""
        return self._vehicle._data["charge_state"]["charge_rate"]

    @property
    def to_max_range(self) -> bool:
        """The max charge range to 100%."""
        return self._vehicle._data["charge_state"]["charge_to_max_range"]

    @property
    def actual_current(self) -> int:
        """The charge speed in kWh."""
        return self._vehicle._data["charge_state"]["charger_actual_current"]

    @property
    def phases(self) -> Union[None, int]: # FIXME
        """How many phases does the car charge with."""
        return self._vehicle._data["charge_state"]["charger_phases"]

    @property
    def pilot_current(self) -> int:
        """The charge speed in amps."""
        return self._vehicle._data["charge_state"]["charger_pilot_current"]

    @property
    def power(self) -> int:
        """Charge power in kWh"""
        return self._vehicle._data["charge_state"]["charger_power"]

    @property
    def voltage(self) -> int:
        """Charge power in kWh"""
        return self._vehicle._data["charge_state"]["charger_voltage"]

    @property
    def charging_state(self) -> str:
        """Charging state

        Returns:
            str: Charging, Disconnected, Stopped
        """
        return self._vehicle._data["charge_state"]["charging_state"]

    @property
    def conn_charge_cable(self) -> str:
        """Charge cable connection?

        Note: Only seen ICE so far.

        Returns:
            str: IEC
        """
        return self._vehicle._data["charge_state"]["conn_charge_cable"]

    @property
    def fast_charger_brand(self) -> str:
        """Fast charger brand

        Note: Dunno what this is, if  you know please update the docs.


        Returns:
            str: Description
        """
        return self._vehicle._data["charge_state"]["fast_charger_brand"]

    @property
    def fast_charger_present(self) -> bool:
        return self._vehicle._data["charge_state"]["fast_charger_present"]

    @property
    def fast_charger_type(self) -> str:
        return self._vehicle._data["charge_state"]["fast_charger_type"]

    @property
    def managed_charging_active(self) -> bool:
        """Is managed charing active."""
        return self._vehicle._data["charge_state"]["managed_charging_active"]

    @property
    def managed_charging_start_time(self) -> Optional[datetime]:
        """When the the charger should start charging.

        Returns:
            Optional[datetime]:
        """
        value = self._vehicle._data["charge_state"]["managed_charging_start_time"]
        if value is not None:
            # Just assuming that the time is like the timestamps.
            return datetime.utcfromtimestamp(value / 1000)

    @property
    def managed_charging_user_canceled(self) -> bool:
        """Returns True if the scheduled_charging_pending has been canceled by the user."""
        return self._vehicle._data["charge_state"]["managed_charging_user_canceled"]

    @property
    def max_range_charge_counter(self) -> int:
        """How many times the car has been charged to MAX Range?"""
        return self._vehicle._data["charge_state"]["max_range_charge_counter"]

    @property
    def minutes_to_full_charge(self) -> int:
        """Returns how minutes it's left until the battery reaches soc limit that is used"""
        return self._vehicle._data["charge_state"]["minutes_to_full_charge"]

    @property
    def scheduled_charging_pending(self) -> bool:
        """Schedule charing pending

        Returns:
            bool: True if there is a charge scheduled_charging_start_time.
        """
        return self._vehicle._data["charge_state"]["scheduled_charging_pending"]

    @property
    def scheduled_charging_start_time(self) -> Optional[datetime]:
        value =  self._vehicle._data["charge_state"]["scheduled_charging_start_time"]
        if value is not None:
            # Just assuming that the time is like the timestamps.
            return datetime.utcfromtimestamp(value / 1000)
        return

    @property
    def fully_charged_at(self) -> datetime:
        """Returns a datetime for when the battery reaches soc limit that is used"""
        return self.timestamp + timedelta(minutes=self.minutes_to_full_charge)

    @property
    def timestamp(self) -> datetime:
        """Datetime from the last time the data was updated."""
        value = self._vehicle._data["charge_state"]["timestamp"]
        return datetime.utcfromtimestamp(value / 1000)

    @property
    def trip_charging(self) -> bool:
        """Trip charging."""
        return self._vehicle._data["charge_state"]["trip_charging"]

    @property
    def user_charge_enable_request(self) -> None:
        # Wtf is this used for?
        return self._vehicle._data["charge_state"]["user_charge_enable_request"]
