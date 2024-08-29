from abc import ABC
from typing import Optional


class DynamicAttrsFactory(ABC):
    data_to_import: list[str] = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if hasattr(cls, "data_to_import"):
            cls._initialize_dynamic_attrs()

    @classmethod
    def _initialize_dynamic_attrs(cls):
        for var_name in cls.data_to_import:
            # Dynamically add type hints
            var_name = var_name.lower()
            cls.__annotations__[var_name] = Optional[str]
            # Initialize attributes to None
            setattr(cls, var_name, None)
