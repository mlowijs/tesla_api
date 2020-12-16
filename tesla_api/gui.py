from datetime import datetime

from .base import Stub


class Gui(Stub):

    """Gui related thing like what format the Vehicle uses for range, time etc
    """

    __key = "gui_settings"

    @property
    def twenty_four_hour(self) -> bool:
        """Returns True if the car uses 00:00 format."""
        return self._vehicle._data[self.__key]["gui_24_hour_time"]

    @property
    def charge_rate_unit(self) -> str:
        """What charge rate unit is used on the gui

        Returns:
            str: kW, km/hr m/hr
        """
        return self._vehicle._data[self.__key]["gui_charge_rate_units"]

    @property
    def distance_unit(self) -> str:
        """Distance unit the vehicle uses in the gui

        Note: Not sure about the the american format, mph, mi/h

        Returns:
            str: km/hr, m/hr
        """
        return self._vehicle._data[self.__key]["gui_distance_units"]

    @property
    def temperature_unit(self) -> str:
        """temperature_unit the vehicle uses in the gui

        Returns:
            str: C or F
        """
        return self._vehicle._data[self.__key]["gui_temperature_units"]

    @property
    def range_unit(self) -> bool:
        """Range unit

        Returns:
            bool: Rated, todo list the other values...
        """
        return self._vehicle._data[self.__key]["gui_range_display"]

    @property
    def last_update(self) -> datetime:
        value = self._vehicle._data[self.__key]["timestamp"]
        return datetime.utcfromtimestamp(value / 1000)
