from functools import partialmethod

from .base import Stub
from .doors import Doors
from .sentry import Sentry
from .speedlimit import Speedlimit
from .trunks import Trunks
from .windows import Windows


class Controls(Stub):
    def __init__(self, vehicle):
        super().__init__(vehicle)
        self.doors = Doors(vehicle)
        self.windows = Windows(vehicle)
        self.speedlimit = Speedlimit(vehicle)
        self.trunks = Trunks(vehicle)
        self.sentry = Sentry(vehicle)

    async def _set_sunroof_state(self, state):
        return await self._vehicle._command("sun_roof_control", {"state": state})

    vent_sunroof = partialmethod(_set_sunroof_state, "vent")
    close_sunroof = partialmethod(_set_sunroof_state, "close")

    async def flash_lights(self):
        """Flash front lights."""
        return await self._vehicle._command("flash_lights")

    async def honk_horn(self):
        """Honk the horn."""
        return await self._vehicle._command("honk_horn")

    async def set_valet_mode(self, on: bool = True, password=""):
        """Turn on or off valet mode.

        Valet Mode limits the car's top speed to 70MPH and 80kW of acceleration power. It also disables Homelink, Bluetooth and Wifi settings, and the ability to disable mobile access to the car. It also hides your favorites, home, and work locations in navigation.

        parameters:
            on (bool): True to activate, False to deactiveate
            password (str): A PIN to deactivate Valet Mode

        Note:
            password parameter isn't required to turn on or off Valet Mode, even with a previous PIN set.
            If you clear the PIN and activate Valet Mode without the parameter, you will only be able to deactivate it from your car's screen by signing into your Tesla account


        """
        pwd = password or self._vehicle._api_client._password
        return await self._vehicle._command(
            "set_valet_mode", data={"on": on, "password": pwd}
        )
