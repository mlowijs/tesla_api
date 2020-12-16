from .base import Stub
from .misc import cast


class Battery(Stub):
    @property
    def not_enough_power_to_heat(self) -> bool:
        """The soc is to low use the heater.

        Returns:
            bool: Think this is if camping mode if on and power is less then 20%
        """
        return cast(self._vehicle._data["charge_state"]["not_enough_power_to_heat"])

    @property
    def heater_on(self) -> bool:
        """Check if the battery heater is on.

        Returns:
            bool: True if the heater is on
        """
        return self._vehicle._data["charge_state"]["battery_heater_on"]

    @property
    def soc(self) -> int:
        """The returns how many percent that is left on the charge

        Returns:
            int: soc.
        """
        return self._vehicle._data["charge_state"]["battery_level"]

    @property
    def usable_soc(self) -> int:
        """How many percent of soc is available for usage.

        Returns:
            int:
        """
        return self._vehicle._data["charge_state"]["usable_battery_level"]

    @property
    def range(self) -> float:
        """Range in the distance unit used by the car

        Returns:
            float: How many miles/km you can drive before you have to call triple A
        """
        value = self._vehicle._data["charge_state"]["battery_range"]
        return self._vehicle._format_distance_unit(value)

    @property
    def estimated_range(self) -> float:
        """Range in the distance unit used by the car

        Returns:
            float: How many miles/km you can drive before you have to call triple A
        """
        value = self._vehicle._data["charge_state"]["est_battery_range"]
        return self._vehicle._format_distance_unit(value)

    @property
    def ideal_range(self) -> float:
        """Range in the distance unit used by the car

        Returns:
            float: How many miles/km you can drive before you have to call triple A
        """
        value = self._vehicle._data["charge_state"]["ideal_battery_range"]
        return self._vehicle._format_distance_unit(value)
