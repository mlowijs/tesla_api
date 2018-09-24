class Climate:
    def __init__(self, api_client):
        self._api_client = api_client

    def get_climate_state(self, vehicle_id):
        return self._api_client.get(f'vehicles/{vehicle_id}/data_request/climate_state')

    def start_climate(self, vehicle_id):
        return self._api_client.post(f'vehicles/{vehicle_id}/command/auto_conditioning_start')

    def stop_climate(self, vehicle_id):
        return self._api_client.post(f'vehicles/{vehicle_id}/command/auto_conditioning_stop')

    # def set_temperatures(self, vehicle_id, driver_temperature, passenger_temperature = None):
    #     passenger_temperature = driver_temperature if passenger_temperature is None else passenger_temperature
    #     return self._api_client.post(f'vehicles/{vehicle_id}/command/set_temps?driver_temp={driver_temperature}&passenger_temp={passenger_temperature}')
