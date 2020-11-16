from datetime import datetime

from .base import Stub


class Config(Stub):
    __key = "vehicle_config"

    @property
    def can_accept_navigation_requests(self) -> bool:
        return self._vehicle._data[self.__key]["can_accept_navigation_requests"]

    @property
    def can_actuate_trunks(self) -> bool:
        return self._vehicle._data[self.__key]["can_actuate_trunks"]

    @property
    def car_special_type(self) -> str:
        return self._vehicle._data[self.__key]["car_special_type"]

    @property
    def car_type(self) -> str:
        return self._vehicle._data[self.__key]["car_type"]

    @property
    def charge_port_type(self) -> str:
        return self._vehicle._data[self.__key]["charge_port_type"]

    @property
    def default_charge_to_max(self) -> str:
        return self._vehicle._data[self.__key]["default_charge_to_max"]

    @property
    def ece_restrictions(self) -> bool:
        """ece_restrictions"""
        return self._vehicle._data[self.__key]["ece_restrictions"]

    @property
    def eu_vehicle(self) -> bool:
        """EU version of the vedicle"""
        return self._vehicle._data[self.__key]["eu_vehicle"]

    @property
    def exterior_color(self) -> str:
        """EU version of the vedicle"""
        return self._vehicle._data[self.__key]["exterior_color"]

    @property
    def exterior_trim(self) -> str:
        """EU version of the vedicle"""
        return self._vehicle._data[self.__key]["exterior_trim"]

    @property
    def has_air_suspension(self) -> bool:
        """EU version of the vedicle"""
        return self._vehicle._data[self.__key]["has_air_suspension"]

    @property
    def has_ludicrous_mode(self) -> bool:
        """EU version of the vedicle"""
        return self._vehicle._data[self.__key]["has_ludicrous_mode"]

    @property
    def key_version(self) -> int:
        """Key version."""
        return self._vehicle._data[self.__key]["key_version"]

    @property
    def motorized_charge_port(self) -> bool:
        """Key version."""
        return self._vehicle._data[self.__key]["motorized_charge_port"]

    @property
    def plg(self) -> bool:
        """U have no fucking idea what this is about."""
        return self._vehicle._data[self.__key]["plg"]

    @property
    def rear_seat_heaters(self) -> int:
        """If the car has read seat heaters."""
        return self._vehicle._data[self.__key]["rear_seat_heaters"]

    @property
    def rear_seat_type(self) -> int:
        """If the car has read seat heaters."""
        return self._vehicle._data[self.__key]["rear_seat_type"]

    @property
    def right_hand_drive(self) -> bool:
        """Right hand drive model"""
        return self._vehicle._data[self.__key]["rhd"]

    @property
    def roof_color(self) -> str:
        """Roof color."""
        return self._vehicle._data[self.__key]["roof_color"]

    @property
    def seat_type(self) -> str:
        """Roof color."""
        return self._vehicle._data[self.__key]["seat_type"]

    @property
    def spoiler_type(self) -> str:
        """Roof color."""
        return self._vehicle._data[self.__key]["spoiler_type"]

    @property
    def sun_roof_installed(self) -> str:
        """Roof color."""
        return self._vehicle._data[self.__key]["sun_roof_installed"]

    @property
    def third_row_seats(self) -> str:
        """Third row seats"""
        return self._vehicle._data[self.__key]["third_row_seats"]

    @property
    def use_range_badging(self) -> bool:
        """#TODO"""
        return self._vehicle._data[self.__key]["use_range_badging"]

    @property
    def wheel_type(self) -> str:
        """Wheel type. Pinwheel18"""
        return self._vehicle._data[self.__key]["wheel_type"]

    @property
    def last_update(self) -> datetime:
        value = self._vehicle._data[self.__key]["timestamp"]
        return datetime.utcfromtimestamp(value / 1000)
