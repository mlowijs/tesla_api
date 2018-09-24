class State:
    def __init__(self, api_client, vehicle_id):
        self._api_client = api_client
        self._vehicle_id = vehicle_id

    def is_mobile_enabled(self):
        return self._api_client.get(f'vehicles/{self._vehicle_id}/mobile_enabled')

    def get_vehicle_state(self):
        return self._api_client.get(f'vehicles/{self._vehicle_id}/data_request/vehicle_state')

    def get_drive_state(self):
        return self._api_client.get(f'vehicles/{self._vehicle_id}/data_request/drive_state')

    def get_gui_settings(self):
        return self._api_client.get(f'vehicles/{self._vehicle_id}/data_request/gui_settings')

    def wake_up_vehicle(self):
        return self._api_client.post(f'vehicles/{self._vehicle_id}/wake_up')