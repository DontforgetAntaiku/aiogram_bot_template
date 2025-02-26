import logging
from typing import Optional

from dotenv import load_dotenv

from app.services.classes import ConfigFactory, SingletonFactory


class TgBotInfo(ConfigFactory):
    BOT_TOKEN: str
    REDIS_HOST: str
    REDIS_PORT: int


class DatabaseInfo(ConfigFactory):
    DB_USER: str
    DB_PASSWORD: Optional[str]
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str


class WebhookInfo(ConfigFactory):
    WEB_SERVER_HOST: str
    WEB_SERVER_PORT: int
    WEBHOOK_PATH: str
    BASE_URL: str
    X_Telegram_Bot_Api_Secret_Token: str


class Config(SingletonFactory):
    TgBot: TgBotInfo
    DataBase: DatabaseInfo
    Webhook: WebhookInfo

    def init(self, path: Optional[str] = None):
        try:
            load_dotenv(path)
            for attr_name, factory_cls in self.__annotations__.items():
                instance = factory_cls()
                instance.init()
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
