from typing import TYPE_CHECKING, cast

from .datatypes import ChargeStateResponse

if TYPE_CHECKING:
    from .vehicle import Vehicle


class Charge:
    def __init__(self, vehicle: "Vehicle"):
        self._vehicle = vehicle
        self._api_client = vehicle._api_client

    async def get_state(self) -> ChargeStateResponse:
        endpoint = "vehicles/{}/data_request/charge_state".format(self._vehicle.id)
        return cast(ChargeStateResponse, await self._api_client.get(endpoint))

    async def start_charging(self) -> bool:
        return cast(bool, await self._vehicle._command("charge_start"))

    async def stop_charging(self) -> bool:
        return cast(bool, await self._vehicle._command("charge_stop"))

    async def set_charge_limit(self, percentage: int) -> bool:  # TODO: int or float?
        percentage = round(percentage)

        if not (50 <= percentage <= 100):
            raise ValueError("Percentage should be between 50 and 100")

        args = {"percent": percentage}
        return cast(bool, await self._vehicle._command("set_charge_limit", args))
