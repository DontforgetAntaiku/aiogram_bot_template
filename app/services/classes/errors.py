class EnvironmentError(Exception):
    def __init__(self, message):
        self.message = message


class NoParameterError(EnvironmentError):
    pass


class InvalidEnvironmentError(EnvironmentError):
    pass
