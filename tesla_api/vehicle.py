from .charge import Charge
from .climate import Climate
from .controls import Controls    

class Vehicle:
    def __init__(self, api_client, vehicle):
        self._api_client = api_client
        self._vehicle = vehicle

        self._charge = Charge(self._api_client, vehicle['id'])
        self._climate = Climate(self._api_client, vehicle['id'])
        self._controls = Controls(self._api_client, vehicle['id'])

    def is_mobile_access_enabled(self):
        return self._api_client.get('vehicles/{}/mobile_enabled'.format(self.id))

    def get_data(self):
        return self._api_client.get('vehicles/{}/vehicle_data'.format(self.id))

    def get_state(self):
        return self._api_client.get('vehicles/{}/data_request/vehicle_state'.format(self.id))

    def get_drive_state(self):
        return self._api_client.get('vehicles/{}/data_request/drive_state'.format(self.id))

    def get_gui_settings(self):
        return self._api_client.get('vehicles/{}/data_request/gui_settings'.format(self.id))

    def wake_up(self):
        return self._api_client.post('vehicles/{}/wake_up'.format(self.id))

    @property
    def id(self):
        return self._vehicle['id']

    @property
    def display_name(self):
        return self._vehicle['display_name']

    @property
    def vin(self):
        return self._vehicle['vin']

    @property
    def state(self):
        return self._vehicle['state']

    @property
    def charge(self):
        return self._charge

    @property
    def climate(self):
        return self._climate

    @property
    def controls(self):
        return self._controls
