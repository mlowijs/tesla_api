class Climate:
    def __init__(self, api_client, vehicle_id):
        self._api_client = api_client
        self._vehicle_id = vehicle_id

    def get_state(self):
        return self._api_client.get('vehicles/{}/data_request/climate_state'.format(self._vehicle_id))

    def start_climate(self):
        return self._api_client.post('vehicles/{}/command/auto_conditioning_start'.format(self._vehicle_id))

    def stop_climate(self):
        return self._api_client.post('vehicles/{}/command/auto_conditioning_stop'.format(self._vehicle_id))

    def set_temperature(self, driver_temperature, passenger_temperature = None):
        return self._api_client.post(
            'vehicles/{}/command/set_temps'.format(self._vehicle_id),
            {'driver_temp': driver_temperature,
             'passenger_temp': passenger_temperature or driver_temperature}
        )
