class Stub:

    def __init__(self, vehicle):
        self._vehicle = vehicle
        self._api_client = vehicle._api_client

    async def refresh(self):
        # Refresh for all stubs, if the child has a way to only pull info that
        # related to there class overwritten.
        return await self._vehicle.full_update()
