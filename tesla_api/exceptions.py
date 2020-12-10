from aiohttp.client_exceptions import ClientConnectionError as ClientError

class AuthenticationError(Exception):
    def __init__(self, error: object):
        super().__init__('Authentication to the Tesla API failed: {}'.format(error))

class ApiError(Exception):
    def __init__(self, error: object):
        super().__init__('Tesla API call failed: {}'.format(error))
        self.reason = error

class VehicleUnavailableError(Exception):
    def __init__(self) -> None:
        super().__init__('Vehicle failed to wake up.')

class VehicleInServiceError(VehicleUnavailableError):
    def __init__(self) -> None:
        Exception.__init__(self, 'Vehicle is currently in service.')
