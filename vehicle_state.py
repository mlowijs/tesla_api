class VehicleState:
    def __init__(self, api_client):
        self._api_client = api_client

    def is_mobile_enabled(self, vehicle_id):
        return self._api_client.get(f'vehicles/{vehicle_id}/mobile_enabled')

    def get_vehicle_state(self, vehicle_id):
        return self._api_client.get(f'vehicles/{vehicle_id}/data_request/vehicle_state')

    def get_drive_state(self, vehicle_id):
        return self._api_client.get(f'vehicles/{vehicle_id}/data_request/drive_state')

    def get_gui_settings(self, vehicle_id):
        return self._api_client.get(f'vehicles/{vehicle_id}/data_request/gui_settings')

    def wake_up_vehicle(self, vehicle_id):
        return self._api_client.post(f'vehicles/{vehicle_id}/wake_up')