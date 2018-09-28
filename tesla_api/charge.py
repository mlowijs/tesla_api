class Charge:
    def __init__(self, api_client, vehicle_id):
        self._api_client = api_client
        self._vehicle_id = vehicle_id

    def get_state(self):
        return self._api_client.get('vehicles/{}/data_request/charge_state'.format(self._vehicle_id))

    def start_charging(self):
        return self._api_client.post('vehicles/{}/command/charge_start'.format(self._vehicle_id))

    def stop_charging(self):
        return self._api_client.post('vehicles/{}/command/charge_stop'.format(self._vehicle_id))

    def set_charge_limit(self, percentage):
        percentage = round(percentage)

        if percentage < 50 or percentage > 100:
            raise ValueError('Percentage should be between 50 and 100')

        return self._api_client.post(
            'vehicles/{}/command/set_charge_limit'.format(self._vehicle_id),
            {'percent': percentage}
        )