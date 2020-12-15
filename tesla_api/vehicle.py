import asyncio

from .charge import Charge
from .climate import Climate
from .controls import Controls
from .exceptions import ApiError, VehicleUnavailableError


class Vehicle:
    def __init__(self, api_client, vehicle):
        self._api_client = api_client
        self._vehicle = vehicle

        self.charge = Charge(self)
        self.climate = Climate(self)
        self.controls = Controls(self)

    async def _command(self, command_endpoint, data=None, _retry=True):  # noqa: C901
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
            res = await self._api_client.post(endpoint, data)
        except VehicleUnavailableError:
            # If first attempt, retry with a wake up.
            if _retry:
                self._vehicle["state"] = "offline"
                return await self._command(command_endpoint, data, _retry=False)
            raise

        if res.get("result") is not True:
            raise ApiError(res.get("reason", ""))

    def _update_vehicle(self, state):
        self._vehicle = state
        if self._api_client.callback_update is not None:
            asyncio.create_task(self._api_client.callback_update(self))

    async def is_mobile_access_enabled(self):
        return await self._api_client.get("vehicles/{}/mobile_enabled".format(self.id))

    async def get_data(self):
        data = await self._api_client.get("vehicles/{}/vehicle_data".format(self.id))
        self._update_vehicle({k: v for k, v in data.items() if not isinstance(v, dict)})
        return data

    async def get_state(self):
        return await self._api_client.get(
            "vehicles/{}/data_request/vehicle_state".format(self.id))

    async def get_drive_state(self):
        return await self._api_client.get(
            "vehicles/{}/data_request/drive_state".format(self.id))

    async def get_gui_settings(self):
        return await self._api_client.get(
            "vehicles/{}/data_request/gui_settings".format(self.id))

    async def wake_up(self, timeout=-1):  # noqa: C901
        """Attempt to wake up the car.

        Vehicle will be online when this function returns successfully.

        Args:
            timeout: Seconds to keep attempting wakeup. Set to None to run until complete.
                Defaults to timeout attribute on TeslaApiClient.

        Raises:
            VehicleUnavailableError: Timeout exceeded without success.
        """
        if timeout is None:
            delay = 2
        else:
            if timeout <= 0:
                timeout = self._api_client.timeout
            delay = timeout / 100

        async def _wake():
            state = await self._api_client.post("vehicles/{}/wake_up".format(self.id))
            self._update_vehicle(state)
            while self._vehicle["state"] != "online":
                await asyncio.sleep(delay)
                state = await self._api_client.post("vehicles/{}/wake_up".format(self.id))
                self._update_vehicle(state)

        if self._api_client.callback_wake_up is not None:
            asyncio.create_task(self._api_client.callback_wake_up(self))

        try:
            await asyncio.wait_for(_wake(), timeout)
        except asyncio.TimeoutError:
            raise VehicleUnavailableError()

    async def remote_start(self, password):
        """Enable keyless driving (must start car within a 2 minute window).

        password - The account password to reauthenticate.
        """
        return await self._command("remote_start_drive", data={"password": password})

    async def update(self):
        self._update_vehicle(await self._api_client.get("vehicles/{}".format(self.id)))

    def __dir__(self):
        """Include _vehicle keys in dir(), which are accessible with __getattr__()."""
        return super().__dir__() | self._vehicle.keys()

    def __getattr__(self, name):
        """Allow attribute access to _vehicle details."""
        try:
            return self._vehicle[name]
        except KeyError:
            raise AttributeError(
                "'{}' object has no attribute '{}'".format(self.__class__.__name__, name))
