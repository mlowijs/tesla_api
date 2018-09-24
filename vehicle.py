class Vehicle:
    def __init__(self, api_client):
        self._api_client = api_client

    def list_vehicles(self):
        return self._api_client.get('vehicles')