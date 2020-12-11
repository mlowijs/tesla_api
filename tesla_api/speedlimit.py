from functools import partialmethod

from .base import Stub


class Speedlimit(Stub):
    @property
    def is_active(self) -> bool:
        return self._vehicle._data["vehicle_state"]["speed_limit_mode"]["active"]

    @property
    def current_limit_mph(self):
        return self._vehicle._data["vehicle_state"]["speed_limit_mode"]["current_limit_mph"]

    @property
    def current_limit(self):
        return self._vehicle._format_distance_unit(self.current_limit_mph)

    @property
    def max_limit_mph(self):
        return self._vehicle._data["vehicle_state"]["speed_limit_mode"]["max_limit_mph"]

    def max_limit(self):
        """Max limit in the gui format"""
        return self._vehicle._format_distance_unit(self.max_limit_mph)

    @property
    def pin_code_set(self):
        return self._vehicle._data["vehicle_state"]["speed_limit_mode"]["pin_code_set"]

    async def set_speed_limit(self, limit: int):
        """Sets the maximum speed allowed when Speed Limit Mode is active."""
        # https://tesla-api.timdorr.com/vehicle/commands/speedlimit
        if 50 <= limit <= 90:
            #
            gui = await self._vehicle.get_gui_settings()
            if gui["gui_distance_units"] == "km/hr":
                # If the car is using km, lets assume they pass that as a parameter to.
                limit = limit * 0.62

            return await self._vehicle._command("speed_limit_set_limit")

        else:
            raise ValueError("limit has to be within 50 - 90MPH")

    async def _speed_limit(self, cmd, pin):
        return await self._vehicle._command(cmd, data={"pin": pin})

    activate_speed_limit = partialmethod(_speed_limit, "speed_limit_activate")
    deactivate_speed_limit = partialmethod(_speed_limit, "speed_limit_deactivate")

    async def clear_speed_limit_pin(self, pin: int):
        """Clears the currently set PIN for Speed Limit Mode."""
        pin = int(pin)
        if (0 <= pin <= 9999) and len(str(pin)) == 4:
            return await self._vehicle._command(
                "speed_limit_clear_pin", data={"pin": pin}
            )
        else:
            raise ValueError("Pin has to be a 4 digit code")
