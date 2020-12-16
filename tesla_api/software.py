from datetime import datetime, timedelta
from typing import Union

from .base import Stub


class Software(Stub):
    @property
    def update_available(self) -> bool:
        """Check if a update is available

        Returns:
            bool: True if a update is available
        """
        return self.download_percent == 100

    @property
    def done_at(self) -> datetime:
        """What time the update is expected to be done.

        Returns:
            datetime: What time the update is expected to be done.
        """
        sec = self._vehicle._data["vehicle_state"]["software_update"][
            "expected_duration_sec"
        ]
        return datetime.now() + timedelta(seconds=sec)

    @property
    def install_percent(self) -> int:
        """How far along the install is"""
        return self._vehicle._data["vehicle_state"]["software_update"]["install_perc"]

    @property
    def download_percent(self) -> int:
        """How far along the install is"""
        return self._vehicle._data["vehicle_state"]["software_update"]["download_perc"]

    @property
    def status(self) -> str:
        """Status""" # TODO check what is listed here before the next update.
        return self._vehicle._data["vehicle_state"]["software_update"]["status"]

    @property
    def version(self) -> str:
        """What version is the update."""
        return self._vehicle._data["vehicle_state"]["software_update"]["version"]

    async def update(self, offset: Union[datetime, int] = 120) -> bool:
        """Start a update.

        Note:
            Carefull running this as you can't drive the car until it's done.

        Args:
            offset (int, datetime): When the update should start.

        """
        if isinstance(offset, datetime):
            offset = offset - datetime.now()
            offset = int(offset.total_seconds())

        data = {"offset_sec", offset}

        return await self._vehicle._command("schedule_software_update", data=data)

    async def cancel_update(self) -> bool:
        """Cancels a software update, if one is scheduled and has not yet started."""
        return await self._vehicle._command("cancel_software_update")
