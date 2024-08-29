import os

from dotenv import load_dotenv

from tgbot.classes import DynamicAttrsFactory, SingletonFactory


class TgBotInfo(SingletonFactory, DynamicAttrsFactory):
    """
    Creates the TgBot object from environment variables.
    """

    data_to_import = [
        "BOT_TOKEN",
        "REDIS_HOST",
        "REDIS_PORT",
    ]

    def init(self):
        for var_name in self.data_to_import:
            if not os.getenv(var_name):
                raise ValueError(f"Environment variable '{var_name}' not set")
            setattr(self, var_name.lower(), os.getenv(var_name))


class DataBaseInfo(SingletonFactory, DynamicAttrsFactory):
    data_to_import = [
        "DB_USER",
        "DB_PASSWORD",
        "DB_HOST",
        "DB_PORT",
        "DB_NAME",
    ]

    def init(self):
        for var_name in self.data_to_import:
            if not os.getenv(var_name):
                raise ValueError(f"Environment variable '{var_name}' not set")
            setattr(self, var_name.lower(), os.getenv(var_name))


# class BaseURL(Singleton):
#     data_to_import = ["BASE_URL"]
#     def init(self):
#         for var_name in self.data_to_import:
#             if not os.getenv(var_name):
#                 raise ValueError(f"Environment variable '{var_name}' not set")
#             setattr(self, var_name.lower(), os.getenv(var_name))


class Config(SingletonFactory, DynamicAttrsFactory):
    """
    The main configuration class that integrates all the other configuration classes.

    This class holds the other configuration classes, providing a centralized point of access for all settings.

    Attributes
    ----------
    tg_bot : TgBot
        Holds the settings related to the Telegram Bot.
    """

    def init(self, path=None):
        load_dotenv(path)
        self.TgBot: TgBotInfo = TgBotInfo()
        self.DataBase: DataBaseInfo = DataBaseInfo()
        # self.admins = tuple(map(int, os.getenv("ADMINS").split(",")))
