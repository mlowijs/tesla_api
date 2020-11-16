from functools import partialmethod

from .base import Stub


class Sentry(Stub):
    def is_active(self) -> bool:
        return self._vehicle._data["vehicle_state"]["sentry_mode"]

    def is_available(self) -> bool:
        return self._vehicle._data["vehicle_state"]["sentry_mode_available"]

    async def enable_sentry_mode(self, on: bool = True):
        """Enable sentry mode."""
        return await self._vehicle._command("set_sentry_mode", data={"on": on})

    disable_sentry_mode = partialmethod(enable_sentry_mode, on=False)
