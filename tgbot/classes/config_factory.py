import os
from abc import ABC

from .errors import InvalidEnvironmentError, NoParameterError
from .singleton import SingletonFactory


class ConfigFactory(SingletonFactory, ABC):
    data_to_import = []
    nullable = []

    def init(self):
        for item in self.data_to_import:
            var_name, var_type = item if isinstance(item, tuple) else (item, str)
            env_value = os.getenv(var_name, "")
            if not env_value and var_name not in self.nullable:
                raise NoParameterError(f"Environment variable '{var_name}' not set")
            try:
                if var_type in (int, float, str):
                    setattr(self, var_name.lower(), var_type(env_value))
                else:
                    setattr(self, var_name.lower(), var_type(env_value.split(",")))
            except ValueError:
                raise InvalidEnvironmentError(
                    f"Environment variable '{var_name}' has an invalid value"
                )
