from dotenv import load_dotenv

from .classes import ConfigFactory, Errors, SingletonFactory


class TgBotInfo(ConfigFactory):
    """
    Creates the TgBot object from environment variables.
    """

    data_to_import = [
        "BOT_TOKEN",
        "REDIS_HOST",
        ("REDIS_PORT", int),
        "X_Telegram_Bot_Api_Secret_Token",
    ]


class DatabaseInfo(ConfigFactory):
    """_summary_

    Attributes:
        db_user (_type_): username
        db_password (_type_): password
        db_host (_type_): hostname
        db_port (_type_): port
        db_name (_type_): name
    """

    data_to_import = [
        "DB_USER",
        "DB_PASSWORD",
        "DB_HOST",
        ("DB_PORT", int),
        "DB_NAME",
    ]
    nullable = ["DB_PASSWORD"]


class WebhookInfo(ConfigFactory):
    data_to_import = [
        ("WEB_SERVER_HOST", str),
        ("WEB_SERVER_PORT", int),
        ("WEBHOOK_PATH", str),
        ("BASE_URL", str),
    ]


class Config(SingletonFactory):
    """_summary_

    Attrs:
        TgBot (_type_): TgBot
        DataBase (_type_): Database
        Webhook (_type_): Webhook

    Raises:
        e: _description_
    """

    attrs = [
        ("TgBot", TgBotInfo),
        ("DataBase", DatabaseInfo),
        ("Webhook", WebhookInfo),
    ]

    def init(self, path=None):
        load_dotenv(path)
        try:
            for i in self.attrs:
                cls, factory = i
                setattr(self, cls, factory())
        except Errors.EnvironmentError as e:
            self.create_example_env()
            raise e

    def create_example_env(
        self,
    ):
        """
        Creates an example.env file with placeholder values.
        """
        params = []
        for _, cls in self.attrs:
            params.append(f"# {_}")
            for i in cls.data_to_import:
                var_name = i[0] if isinstance(i, tuple) else i
                params.append(var_name + "=")
        with open(".env.example", "w") as file:
            file.write("\n".join(params))
        print("Created .env.example file")
