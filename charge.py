class Charge:
    def __init__(self, api_client):
        self._api_client = api_client

    def get_charge_state(self, vehicle_id):
        return self._api_client.get(f'vehicles/{vehicle_id}/data_request/charge_state')

    def start_charging(self, vehicle_id):
        return self._api_client.post(f'vehicles/{vehicle_id}/command/charge_start')

    def stop_charging(self, vehicle_id):
        return self._api_client.post(f'vehicles/{vehicle_id}/command/charge_stop')