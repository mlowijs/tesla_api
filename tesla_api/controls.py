STATE_VENT = 'vent'
STATE_CLOSE = 'close'

class Controls:
    def __init__(self, api_client, vehicle_id):
        self._api_client = api_client
        self._vehicle_id = vehicle_id

    def _set_sunroof_state(self, state):
        return self._api_client.post(f'vehicles/{self._vehicle_id}/command/sun_roof_control', {'state': state})

    def vent_sunroof(self):
        return self._set_sunroof_state(STATE_VENT)
        
    def close_sunroof(self):
        return self._set_sunroof_state(STATE_CLOSE)

    def flash_lights(self):
        return self._api_client.post(f'vehicles/{self._vehicle_id}/command/flash_lights')