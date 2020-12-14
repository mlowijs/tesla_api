from .base import Stub
from .misc import cast


class Battery(Stub):
    @property
    def not_enough_power_to_heat(self) -> bool:
        return cast(self._vehicle._data["charge_state"]["not_enough_power_to_heat"])

    @property
    def heater_on(self) -> bool:
        return self._vehicle._data["charge_state"]["battery_heater_on"]

    @property
    def level(self) -> int:
        return self._vehicle._data["charge_state"]["battery_level"]

    @property
    def soc(self) -> int:
        return self.level

    @property
    def usable_level(self) -> int:
        return self._vehicle._data["charge_state"]["usable_battery_level"]

    @property
    def range(self) -> int:
        # What format
        return self._vehicle._data["charge_state"]["battery_range"]

    @property
    def estimated_range(self) -> int:
        # What format
        return self._vehicle._data["charge_state"]["est_battery_range"]

    @property
    def ideal_range(self) -> int:
        # What format
        return self._vehicle._data["charge_state"]["ideal_battery_range"]
