class Climate:
    def __init__(self, api_client, vehicle_id):
        self._api_client = api_client
        self._vehicle_id = vehicle_id

    def get_state(self):
        return self._api_client.get('vehicles/{}/data_request/climate_state'.format(self._vehicle_id))

    def start_climate(self):
        return self._api_client.post('vehicles/{}/command/auto_conditioning_start'.format(self._vehicle_id))

    def stop_climate(self):
        return self._api_client.post('vehicles/{}/command/auto_conditioning_stop'.format(self._vehicle_id))

    def set_temperature(self, driver_temperature, passenger_temperature = None):
        return self._api_client.post(
            'vehicles/{}/command/set_temps'.format(self._vehicle_id),
            {'driver_temp': driver_temperature,
             'passenger_temp': passenger_temperature or driver_temperature}
        )
    
    def set_seat_heater(self,temp=0,seat=0):
        # temp = The desired level for the heater. (0-3)
        # The desired seat to heat. (0-5)
        # 0 - Driver
        # 1 - Passenger
        # 2 - Rear left
        # 4 - Rear center
        # 5 - Rear right
        return self._api_client.post('vehicles/{}/command/remote_seat_heater_request'.format(self._vehicle_id),{'heater':seat,'level':temp})

    def start_steering_wheel_heater(self):
        return self._api_client.post('vehicles/{}/command/remote_steering_wheel_heater_request'.format(self._vehicle_id),{'on':True})

    def stop_steering_wheel_heater(self):
        return self._api_client.post('vehicles/{}/command/remote_steering_wheel_heater_request'.format(self._vehicle_id),{'on':False})
    
