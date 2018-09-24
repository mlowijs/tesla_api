class Climate:
    def __init__(self, api_client, vehicle_id):
        self._api_client = api_client
        self._vehicle_id = vehicle_id

    def get_climate_state(self):
        return self._api_client.get(f'vehicles/{self._vehicle_id}/data_request/climate_state')

    def start_climate(self):
        return self._api_client.post(f'vehicles/{self._vehicle_id}/command/auto_conditioning_start')

    def stop_climate(self):
        return self._api_client.post(f'vehicles/{self._vehicle_id}/command/auto_conditioning_stop')

    def set_temperature(self, driver_temperature, passenger_temperature = None):
        passenger_temperature = driver_temperature if passenger_temperature is None else passenger_temperature
        return self._api_client.post(f'vehicles/{self._vehicle_id}/command/set_temps', {'driver_temp': driver_temperature, 'passenger_temp': passenger_temperature})
