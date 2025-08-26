import logging
from typing import Optional

from dotenv import load_dotenv

from .utils.classes import ConfigFactory, SingletonFactory

from .utils.classes.errors import EnvironmentError


class BotInfo(ConfigFactory):
    __prefix__ = "BOT_"
    TOKEN: str


class RedisInfo(ConfigFactory):
    __prefix__ = "REDIS_"
    HOST: str
    PORT: int

class DatabaseInfo(ConfigFactory):
    __prefix__ = "DB_"
    USER: str
    PASSWORD: Optional[str]
    HOST: str
    PORT: int
    NAME: str


class WebhookInfo(ConfigFactory):
    __prefix__ = 'WEBHOOK_'
    HOST: str
    PORT: int
    PATH: str
    BASE_URL: str
    X_Telegram_Bot_Api_Secret_Token: str


class Config(SingletonFactory):
    bot: BotInfo
    redis: RedisInfo
    database: DatabaseInfo
    webhook: WebhookInfo

    def init(self, path: Optional[str] = None):
        try:
            load_dotenv(path)
            for attr_name, factory_cls in self.__annotations__.items():
                instance = factory_cls()
                setattr(self, attr_name, instance)
        except EnvironmentError as E:
            logging.error(E)
            self.create_example_env()
            raise E

    def create_example_env(self):
        """
        Creates an example.env file with placeholder values.
        """
        params = []
        for attr_name, factory_cls in self.__annotations__.items():
            params.append(f"# {attr_name}")
            for var_name in factory_cls.__annotations__.keys():
                params.append(f"{var_name}=")
        with open(".env.example", "w") as file:
            file.write("\n".join(params))
        print("Created .env.example file")
