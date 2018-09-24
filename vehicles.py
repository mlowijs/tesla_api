from charge import Charge
from climate import Climate
from controls import Controls
from vehicle_state import VehicleState

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
        self.vehicle_state = VehicleState(self._api_client, vehicle['id'])

        