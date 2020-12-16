from datetime import datetime, timedelta

from .base import Stub


from typing import Union
class Software(Stub):
    @property
    def update_available(self) -> bool:
        return self.download_percent == 100

    @property
    def done_at(self) -> datetime:
        sec = self._vehicle._data["vehicle_state"]["software_update"][
            "expected_duration_sec"
        ]
        return datetime.now() + timedelta(seconds=sec)

    @property
    def install_percent(self) -> int:
        return self._vehicle._data["vehicle_state"]["software_update"]["install_perc"]

    @property
    def download_percent(self) -> int:
        return self._vehicle._data["vehicle_state"]["software_update"]["download_perc"]

    @property
    def status(self) -> str:
        return self._vehicle._data["vehicle_state"]["software_update"]["status"]

    @property
    def version(self) -> str:
        return self._vehicle._data["vehicle_state"]["software_update"]["version"]

    async def update(self, offset: Union[datetime, int] = 120) -> bool:
        """Start a update as a time in the future.

        Args:
            offset (int, datetime)

        """
        if isinstance(offset, datetime):
            offset = offset - datetime.now()
            offset = int(offset.total_seconds())

        data = {"offset_sec", offset}

        return await self._vehicle._command("schedule_software_update", data=data)

    async def cancel_update(self) -> bool:
        """Cancels a software update, if one is scheduled and has not yet started."""
        return await self._vehicle._command("cancel_software_update")