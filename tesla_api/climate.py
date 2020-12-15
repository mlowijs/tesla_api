from functools import partialmethod


class Climate:
    def __init__(self, vehicle):
        self._vehicle = vehicle
        self._api_client = vehicle._api_client

    async def get_state(self):
        return await self._api_client.get(
            "vehicles/{}/data_request/climate_state".format(self._vehicle.id))

    async def start_climate(self):
        return await self._vehicle._command("auto_conditioning_start")

    async def stop_climate(self):
        return await self._vehicle._command("auto_conditioning_stop")

    async def set_temperature(self, driver_temperature, passenger_temperature=None):
        data = {"driver_temp": driver_temperature,
                "passenger_temp": passenger_temperature or driver_temperature}
        return await self._vehicle._command("set_temps", data)

    async def set_seat_heater(self, temp=0, seat=0):
        # temp = The desired level for the heater. (0-3)
        # The desired seat to heat. (0-5)
        # 0 - Driver
        # 1 - Passenger
        # 2 - Rear left
        # 4 - Rear center
        # 5 - Rear right
        return await self._vehicle._command("remote_seat_heater_request",
                                            {"heater": seat, "level": temp})

    async def steering_wheel_heater(self, on: bool):
        return await self._vehicle._command("remote_steering_wheel_heater_request",
                                            {"on": on})

    start_steering_wheel_heater = partialmethod(steering_wheel_heater, True)
    stop_steering_wheel_heater = partialmethod(steering_wheel_heater, False)
