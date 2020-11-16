from datetime import datetime

from .base import Stub


class Gui(Stub):
    __key = "gui_settings"

    @property
    def twenty_four_hour(self) -> bool:
        return self._vehicle._data[self.__key]["gui_24_hour_time"]

    @property
    def charge_rate_units(self):
        return self._vehicle._data[self.__key]["gui_charge_rate_units"]

    @property
    def distance_unit(self):
        return self._vehicle._data[self.__key]["gui_distance_units"]

    @property
    def temperature_unit(self):
        return self._vehicle._data[self.__key]["gui_temperature_units"]

    @property
    def range_units(self) -> bool:
        return self._vehicle._data[self.__key]["gui_range_display"]

    @property
    def last_update(self) -> datetime:
        value = self._vehicle._data[self.__key]["timestamp"]
        return datetime.utcfromtimestamp(value / 1000)
