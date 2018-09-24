class Charge:
    def __init__(self, api_client, vehicle_id):
        self._api_client = api_client
        self._vehicle_id = vehicle_id

    def get_charge_state(self):
        return self._api_client.get(f'vehicles/{self._vehicle_id}/data_request/charge_state')

    def start_charging(self):
        return self._api_client.post(f'vehicles/{self._vehicle_id}/command/charge_start')

    def stop_charging(self):
        return self._api_client.post(f'vehicles/{self._vehicle_id}/command/charge_stop')