import asyncio
from enum import Enum
from functools import partialmethod
from typing import cast, Literal, TYPE_CHECKING

if TYPE_CHECKING:
    from .vehicle import Vehicle


class SunroofState(Enum):
    STATE_VENT = "vent"
    STATE_CLOSE = "close"


class Controls:
    def __init__(self, vehicle: "Vehicle"):
        self._vehicle = vehicle
        self._api_client = vehicle._api_client

    async def _set_sunroof_state(self, state: SunroofState) -> bool:
        args = {"state": state}
        return cast(bool, await self._vehicle._command("sun_roof_control", args))
    vent_sunroof = partialmethod(_set_sunroof_state, SunroofState.STATE_VENT)
    close_sunroof = partialmethod(_set_sunroof_state, SunroofState.STATE_CLOSE)

    async def flash_lights(self) -> bool:
        return cast(bool, await self._vehicle._command("flash_lights"))

    async def honk_horn(self) -> bool:
        return cast(bool, await self._vehicle._command("honk_horn"))

    async def open_charge_port(self) -> bool:
        return cast(bool, await self._vehicle._command("charge_port_door_open"))

    async def door_lock(self) -> bool:
        return cast(bool, await self._vehicle._command("door_lock"))

    async def door_unlock(self) -> bool:
        return cast(bool, await self._vehicle._command("door_unlock"))