from .base import Stub


class Media(Stub):

    @property
    def center_display(self) -> str:
        cd = {
            0: "off",
            2: "normal on",
            3: "charging screen",
            7: "sentry mode",
            8: "dog mode",
        }

        return cd[self._vehicle._data["vehicle_state"]["center_display_state"]]

    async def toggle_media_playback(self) -> bool:
        return await self._vehicle._command('media_toggle_playback')

    async def next_track(self) -> bool:
        return await self._vehicle._command('media_next_track')

    async def prev_track(self) -> bool:
        return await self._vehicle._command('media_prev_track')

    async def next_fav(self) -> bool:
        return await self._vehicle._command('media_next_fav')

    async def prev_fav(self) -> bool:
        return await self._vehicle._command('media_prev_fav')

    async def volume_up(self) -> bool:
        return await self._vehicle._command('media_volume_up')

    async def volume_down(self) -> bool:
        return await self._vehicle._command('media_volume_down')

    def __getattr__(self, name: str) -> bool:
        return self._vehicle._data["vehicle_state"]["media_state"][name]
