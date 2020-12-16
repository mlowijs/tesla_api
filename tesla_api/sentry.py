from functools import partialmethod

from .base import Stub


class Sentry(Stub):
    @property
    def is_active(self) -> bool:
        """"Returns True if sentry mode is active"""
        return self._vehicle._data["vehicle_state"]["sentry_mode"]

    @property
    def is_available(self) -> bool:
        """Returns True if sentry mode is available """
        return self._vehicle._data["vehicle_state"]["sentry_mode_available"]

    async def enable(self, on: bool = True) -> bool:
        """Enable sentry mode

        Args:
            on (bool, optional): True to enable and False to disable.

        Returns:
            bool: True of the command succeeds
        """
        return await self._vehicle._command("set_sentry_mode", data={"on": on})


    async def disable(self, on: bool = True) -> bool:
        """Disable sentry mode."""
        return await self.enable(on=False)
