"""Everything related to the trunks"""
from .base import Stub
from .misc import cast


class Trunks(Stub):
    async def open_trunk(self) -> bool:
        """Open trunk (rear)."""
        return await self._vehicle._command(
            "actuate_trunk", data={"which_trunk": "rear"}
        )

    async def open_frunk(self) -> bool:
        """Open frunk (front)."""
        return await self._vehicle._command(
            "actuate_trunk", data={"which_trunk": "front"}
        )

    @property
    def frunk_open(self) -> bool:
        """Is frunk open"""
        return cast(self._vehicle._data["vehicle_state"]["ft"])

    @property
    def trunk_open(self) -> bool:
        """Is trunk open."""
        return cast(self._vehicle._data["vehicle_state"]["rt"])
