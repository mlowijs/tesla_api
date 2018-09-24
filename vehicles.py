class Vehicles:
    def __init__(self, api_client):
        self._api_client = api_client

    def list(self):
        return self._api_client.get('vehicles')