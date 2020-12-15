class Charge:
    def __init__(self, vehicle):
        self._vehicle = vehicle
        self._api_client = vehicle._api_client

    async def get_state(self):
        return await self._api_client.get(
            "vehicles/{}/data_request/charge_state".format(self._vehicle.id))

    async def start_charging(self):
        return await self._vehicle._command("charge_start")

    async def stop_charging(self):
        return await self._vehicle._command("charge_stop")

    async def set_charge_limit(self, percentage):
        percentage = round(percentage)

        if not (50 <= percentage <= 100):
            raise ValueError("Percentage should be between 50 and 100")

        return await self._vehicle._command("set_charge_limit", {"percent": percentage})
