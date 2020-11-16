

class Stub:

    def __init__(self, vehicle):
        self._vehicle = vehicle
        self._api_client = vehicle._api_client

    async def refresh(self):
        # select a name and stick with it.
        await self._vehicle.full_update()


class Base:
    def __init__(self, data):
        self._data = data
