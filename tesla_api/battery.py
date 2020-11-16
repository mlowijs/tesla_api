from .base import Stub


class Battery(Stub):
    @property
    def heater_on(self):
        return self._vehicle.data["charge_state"]["battery_heater_on"]

    @property
    def level(self) -> int:
        return self._vehicle.data["charge_state"]["battery_level"]

    @property
    def soc(self) -> int:
        return self.level

    @property
    def usable_level(self) -> int:
        return self._vehicle.data["charge_state"]["usable_battery_level"]

    @property
    def range(self) -> int:
        # What format
        return self._vehicle.data["charge_state"]["battery_range"]

    @property
    def estimated_range(self) -> int:
        # What format
        return self._vehicle.data["charge_state"]["est_battery_range"]

    @property
    def ideal_range(self) -> int:
        # What format
        return self._vehicle.data["charge_state"]["ideal_battery_range"]
