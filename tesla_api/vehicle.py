import asyncio
from typing import cast, Any, Iterable, List, Mapping, Optional, TYPE_CHECKING

from .charge import Charge
from .climate import Climate
from .controls import Controls
from .datatypes import CommandResponse, DriveStateResponse, GUISettingsResponse, VehicleDataResponse, VehiclesIdResponse, VehicleState, VehicleStateResponse
from .exceptions import ApiError, VehicleUnavailableError

if TYPE_CHECKING:
    from . import TeslaApiClient


class Vehicle:
    id: int
    user_id: Optional[int]  # Only available when car is awake.
    vehicle_id: int
    vin: str
    display_name: str
    option_codes: str
    color: None
    tokens: List[str]
    state: VehicleState
    in_service: bool
    id_s: str
    calendar_enabled: bool
    api_version: int
    backseat_token: None
    backseat_token_updated_at: None

    def __init__(self, api_client: 'TeslaApiClient', vehicle: VehiclesIdResponse):
        self._api_client = api_client
        self._vehicle = vehicle

        self.charge = Charge(self)
        self.climate = Climate(self)
        self.controls = Controls(self)

    async def _command(self, command_endpoint: str, data: Optional[Mapping[str, object]] = None,
                       _retry: bool = True) -> None:
        """Handles vehicle commands with the common reason/result response.

        Args:
            command_endpoint: The final part of the endpoint (after /command/).
            data: Optional JSON data to send with the request.

        Raises:
            ApiError on unsuccessful response.
        """
        # Commands won't work if car is offline, so try and wake car first.
        if self.state != "online":
            await self.wake_up()

        endpoint = "vehicles/{}/command/{}".format(self.id, command_endpoint)
        try:
            res = cast(CommandResponse, await self._api_client.post(endpoint, data))
        except VehicleUnavailableError:
            # If first attempt, retry with a wake up.
            if _retry:
                self._vehicle["state"] = "offline"
                await self._command(command_endpoint, data, _retry=False)
            raise

        if res.get("result") is not True:
            raise ApiError(res.get("reason", ""))

    def _update_vehicle(self, state: VehiclesIdResponse) -> None:
        self._vehicle = state
        # Ensure user_id is set if car is not awake.
        self._vehicle.setdefault("user_id", None)  # type: ignore[arg-type,misc]

        if self._api_client.callback_update is not None:
            asyncio.create_task(self._api_client.callback_update(self))

    async def is_mobile_access_enabled(self) -> bool:
        return cast(bool, await self._api_client.get("vehicles/{}/mobile_enabled".format(self.id)))

    async def get_data(self) -> VehicleDataResponse:
        endpoint = "vehicles/{}/vehicle_data".format(self.id)
        data = cast(VehicleDataResponse, await self._api_client.get(endpoint))

        vehicle = cast(VehiclesIdResponse, {k: v for k,v in data.items() if not isinstance(v, dict)})
        self._update_vehicle(vehicle)

        return data

    async def get_state(self) -> VehicleStateResponse:
        endpoint = "vehicles/{}/data_request/vehicle_state".format(self.id)
        return cast(VehicleStateResponse, await self._api_client.get(endpoint))

    async def get_drive_state(self) -> DriveStateResponse:
        endpoint = "vehicles/{}/data_request/drive_state".format(self.id)
        return cast(DriveStateResponse, await self._api_client.get(endpoint))

    async def get_gui_settings(self) -> GUISettingsResponse:
        endpoint = "vehicles/{}/data_request/gui_settings".format(self.id)
        return cast(GUISettingsResponse, await self._api_client.get(endpoint))

    async def wake_up(self, timeout: Optional[float] = -1) -> None:
        """Attempt to wake up the car.

        Vehicle will be online when this function returns successfully.

        Args:
            timeout: Seconds to keep attempting wakeup. Set to None to run until complete.
                Defaults to timeout attribute on TeslaApiClient.

        Raises:
            VehicleUnavailableError: Timeout exceeded without success.
        """
        delay: float
        if timeout is None:
            delay = 2
        else:
            if timeout <= 0:
                timeout = self._api_client.timeout
            delay = timeout / 100

        async def _wake() -> None:
            endpoint = "vehicles/{}/wake_up".format(self.id)
            state = cast(VehiclesIdResponse, await self._api_client.post(endpoint))
            self._update_vehicle(state)
            while self._vehicle["state"] != "online":
                await asyncio.sleep(delay)
                state = cast(VehiclesIdResponse, await self._api_client.post(endpoint))
                self._update_vehicle(state)

        if self._api_client.callback_wake_up is not None:
            asyncio.create_task(self._api_client.callback_wake_up(self))

        try:
            await asyncio.wait_for(_wake(), timeout)
        except asyncio.TimeoutError:
            raise VehicleUnavailableError()

    async def remote_start(self, password: str) -> bool:
        """Enable keyless driving (must start car within a 2 minute window).

        password - The account password to reauthenticate.
        """
        return cast(bool, await self._command("remote_start_drive", {"password": password}))

    async def update(self) -> None:
        endpoint = "vehicles/{}".format(self.id)
        vehicle = cast(VehiclesIdResponse, await self._api_client.get(endpoint))
        self._update_vehicle(vehicle)

    def __dir__(self) -> Iterable[str]:
        """Include _vehicle keys in dir(), which are accessible with __getattr__()."""
        return super().__dir__() | self._vehicle.keys()

    def __getattr__(self, name: str) -> Any:  # type: ignore[misc]
        """Allow attribute access to _vehicle details."""
        try:
            return self._vehicle[name]  # type: ignore[misc]
        except KeyError:
            raise AttributeError(
                "'{}' object has no attribute '{}'".format(self.__class__.__name__, name))
