from functools import partialmethod
from typing import Optional

from .base import Stub
from .doors import Doors
from .sentry import Sentry
from .software import Software
from .speedlimit import Speedlimit
from .trunks import Trunks
from .windows import Windows


class Controls(Stub):
    def __init__(self, vehicle: "Vehicle") -> None:
        super().__init__(vehicle)
        self.doors = Doors(vehicle)
        self.windows = Windows(vehicle)
        self.speedlimit = Speedlimit(vehicle)
        self.trunks = Trunks(vehicle)
        self.sentry = Sentry(vehicle)
        self.software = Software(vehicle)

    async def _set_sunroof_state(self, state: str) -> bool:
        """ Controls the panoramic sunroof on the Model S. """
        return await self._vehicle._command("sun_roof_control", {"state": state})

    vent_sunroof = partialmethod(_set_sunroof_state, "vent")
    close_sunroof = partialmethod(_set_sunroof_state, "close")

    async def flash_lights(self) -> bool:
        """Flash front lights."""
        return await self._vehicle._command("flash_lights")

    async def homelink(self, lat=Optional[float], lon=Optional[float]) -> True:
        """Opens or closes the primary Homelink device. The provided location must be in proximity of stored location of the Homelink device."""
        lat = lat or self._vehicle._data["drive_state"]["latitude"]
        lon = lon or self._vehicle._data["drive_state"]["longitude"]
        data = {"lat": lat, "lon": lon}

        return await self._vehicle._command("trigger_homelink", data=data)

    async def honk_horn(self) -> bool:
        """Honk the horn."""
        return await self._vehicle._command("honk_horn")

    async def set_valet_mode(self, on: bool = True, password: str = "") -> bool:
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
