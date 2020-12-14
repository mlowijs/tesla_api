from functools import partialmethod

from .base import Stub


class Sentry(Stub):
    @property
    def is_active(self) -> bool:
        return self._vehicle._data["vehicle_state"]["sentry_mode"]

    @property
    def is_available(self) -> bool:
        return self._vehicle._data["vehicle_state"]["sentry_mode_available"]

    # Should probable check and rename methods
    # I want them to be as close to the class as possible.
    async def enable(self, on: bool = True) -> bool:
        """Enable sentry mode."""
        return await self._vehicle._command("set_sentry_mode", data={"on": on})

    disable = partialmethod(enable, on=False)
