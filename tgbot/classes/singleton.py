from abc import ABC, abstractmethod


class SingletonFactory(ABC):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, *args, **kwargs):
        if not hasattr(self, "_initialized"):
            self._initialized = True
            self.init(*args, **kwargs)

    @abstractmethod
    def init(self, *args, **kwargs):
        """
        Subclasses must override this method for initialization.
        """
        raise NotImplementedError


# example
# class Bot(Singleton):
#     def init(self, *args, **kwargs):
#         # Ensure this method is called only once
#         print("Bot initialized with args:", args, "and kwargs:", kwargs)
#         self.settings = kwargs.get('settings', {})
#         for i in args:
#             setattr(self, f"arg_{i}", i)
