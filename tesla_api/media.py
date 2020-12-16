from .base import Stub


class Media(Stub):

    """Stuff related to the Media and media playback.
    """

    @property
    def center_display(self) -> str:
        """Indicate what's on the screen.

        Returns:
            str: Possible values off, normal on, charing screen, sentry mode, dog mode
        """
        cd = {
            0: "off",
            2: "normal on",
            3: "charging screen",
            7: "sentry mode",
            8: "dog mode",
        }

        return cd[self._vehicle._data["vehicle_state"]["center_display_state"]]

    async def toggle_media_playback(self) -> bool:
        """Toggle media playback

        Returns:
            bool: True if successfull
        """
        return await self._vehicle._command('media_toggle_playback')

    async def next_track(self) -> bool:
        """Skip to next track

        Returns:
            bool: True if successfull
        """
        return await self._vehicle._command('media_next_track')

    async def prev_track(self) -> bool:
        """Jump back the previous track

        Returns:
            bool: True if successfull
        """
        return await self._vehicle._command('media_prev_track')

    async def next_fav(self) -> bool:
        """Jump to next favorite

        Returns:
            bool: True if successfull
        """
        return await self._vehicle._command('media_next_fav')

    async def prev_fav(self) -> bool:
        """Jump to previous favorite

        Returns:
            bool: True if successfull
        """
        return await self._vehicle._command('media_prev_fav')

    async def volume_up(self) -> bool:
        """Increase the volume

        Returns:
            bool: True if successfull
        """
        return await self._vehicle._command('media_volume_up')

    async def volume_down(self) -> bool:
        """Decrease the volume

        Returns:
            bool: True if successfull
        """
        return await self._vehicle._command('media_volume_down')

    def __getattr__(self, name: str) -> bool:
        return self._vehicle._data["vehicle_state"]["media_state"][name]
