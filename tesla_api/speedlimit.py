from functools import partialmethod

from .base import Stub
from .misc import mile_to_km


class Speedlimit(Stub):
    @property
    def is_active(self) -> bool:
        return self._vehicle._data["vehicle_state"]["speed_limit_mode"]["active"]

    @property
    def current_limit_mph(self) -> float:
        return self._vehicle._data["vehicle_state"]["speed_limit_mode"]["current_limit_mph"]

    @property
    def current_limit(self) -> float:
        return self._vehicle._format_distance_unit(self.current_limit_mph)

    @property
    def max_limit_mph(self) -> int:
        return self._vehicle._data["vehicle_state"]["speed_limit_mode"]["max_limit_mph"]

    def max_limit(self):
        """Max limit in the gui format"""
        return self._vehicle._format_distance_unit(self.max_limit_mph)

    @property
    def pin_code_set(self) -> bool:
        return self._vehicle._data["vehicle_state"]["speed_limit_mode"]["pin_code_set"]

    async def set_speed_limit(self, limit: int):
        """Sets the maximum speed allowed when Speed Limit Mode is active."""
        # https://tesla-api.timdorr.com/vehicle/commands/speedlimit

        min_limit = 50
        max_limit = 90

        try:
            distance_unit = self._vehicle.gui.distance_unit
        except KeyError:
            await self._vehicle.full_update()
            distance_unit = self._vehicle.gui.distance_unit

        if distance_unit == "km/hr":
            min_limit = mile_to_km(50)
            max_limit = mile_to_km(90)


        # convert to km etc.
        if min_limit <= limit <= max_limit:
            # This need to be tested, dunno how this should be passed.
            return await self._vehicle._command("speed_limit_set_limit", data=limit)

        else:
            raise ValueError("limit has to be within 50 - 90MPH")

    async def _speed_limit(self, cmd: str, pin: int) -> bool:
        return await self._vehicle._command(cmd, data={"pin": pin})

    activate_speed_limit = partialmethod(_speed_limit, "speed_limit_activate")
    deactivate_speed_limit = partialmethod(_speed_limit, "speed_limit_deactivate")

    async def clear_speed_limit_pin(self, pin: int) -> bool:
        """Clears the currently set PIN for Speed Limit Mode."""
        pin = int(pin)
        if (0 <= pin <= 9999) and len(str(pin)) == 4:
            return await self._vehicle._command(
                "speed_limit_clear_pin", data={"pin": pin}
            )
        else:
            raise ValueError("Pin has to be a 4 digit code")
