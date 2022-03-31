class AuthenticationError(Exception):
    def __init__(self, error):
        super().__init__("Authentication to the Tesla API failed: {}".format(error))


class ApiError(Exception):
    def __init__(self, error):
        super().__init__("Tesla API call failed: {}".format(error))
        self.reason = error


class VehicleUnavailableError(Exception):
    def __init__(self):
        super().__init__("Vehicle failed to wake up.")


class JWTDecodeError(Exception):
    def __init__(self):
        super().__init__("Unable to decode JWT")
