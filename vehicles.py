from charge import Charge
from climate import Climate
from controls import Controls
from state import State

class Vehicles:
    def __init__(self, api_client):
        self._api_client = api_client

    def list(self):
        return [Vehicle(self._api_client, vehicle) for vehicle in self._api_client.get('vehicles')]

class Vehicle:
    def __init__(self, api_client, vehicle):
        self._api_client = api_client
        self._vehicle = vehicle

        self.charge = Charge(self._api_client, vehicle['id'])
        self.climate = Climate(self._api_client, vehicle['id'])
        self.controls = Controls(self._api_client, vehicle['id'])
        self.state = State(self._api_client, vehicle['id'])

    @property
    def id(self):
        return self._vehicle['id']

    @property
    def display_name(self):
        return self._vehicle['display_name']

    @property
    def vin(self):
        return self._vehicle['vin']

        