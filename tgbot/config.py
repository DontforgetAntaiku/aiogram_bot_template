from dataclasses import dataclass
from typing import List

from environs import Env


@dataclass
class TgBot:
    """
    Creates the TgBot object from environment variables.
    """

    token: str
    redis_host: str
    redis_port: int
    group_id: int
    admins_id: List[int]

    @staticmethod
    def from_env(env: Env):
        """
        Creates the TgBot object from environment variables.
        """
        token = env.str("BOT_TOKEN")
        group_id = env.int("GROUP_ID")
        admins_id = env.list("ADMINS_ID")
        redis_host = env.str("REDIS_HOST")
        redis_port = env.int("REDIS_PORT")
        return TgBot(
            token=token,
            group_id=group_id,
            admins_id=list(map(int, admins_id)),
            redis_host=redis_host,
            redis_port=redis_port,
        )


@dataclass
class Config:
    """
    The main configuration class that integrates all the other configuration classes.

    This class holds the other configuration classes, providing a centralized point of access for all settings.

    Attributes
    ----------
    tg_bot : TgBot
        Holds the settings related to the Telegram Bot.
    """

    tg_bot: TgBot


def load_config(path: str = None) -> Config:
    """
    This function takes an optional file path as input and returns a Config object.
    :param path: The path of env file from where to load the configuration variables.
    It reads environment variables from a .env file if provided, else from the process environment.
    :return: Config object with attributes set as per environment variables.
    """

    # Create an Env object.
    # The Env object will be used to read environment variables.
    env = Env()
    env.read_env(path=path)

    return Config(
        tg_bot=TgBot.from_env(env),
    )
