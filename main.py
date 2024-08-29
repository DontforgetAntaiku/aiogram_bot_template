import asyncio
import logging
import os

import betterlogging as bl
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import DefaultKeyBuilder, Redis, RedisStorage
from aiogram.types import BotCommand

# from aiogram.utils.i18n import ConstI18nMiddleware, I18n
from aiogram_dialog import setup_dialogs

from tgbot.config import Config
from tgbot.db.database import DB
from tgbot.handlers import routers_list
from tgbot.middlewares.config import ConfigMiddleware
from tgbot.middlewares.db import DbMiddleware
from tgbot.middlewares.errors import ErrorMiddleware


def setup_logging():
    log_level = logging.ERROR
    bl.basic_colorized_config(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)
    if logger.hasHandlers():
        logger.handlers.clear()
    file_handler = logging.FileHandler(r"logging.txt")
    file_handler.setLevel(log_level)
    file_formatter = logging.Formatter(
        "%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    logging.getLogger().addHandler(file_handler)
    logging.error("Starting bot")


async def main():
    os.chdir(os.path.dirname(__file__))
    config = Config(".env")
    setup_logging()
    redis = Redis(host=config.TgBot.redis_host, port=config.TgBot.redis_port)
    storage = RedisStorage(redis, key_builder=DefaultKeyBuilder(with_destiny=True))
    database = DB(
        user=config.DataBase.db_user,
        password=config.DataBase.db_password,
        dbname=config.DataBase.db_name,
        host=config.DataBase.db_host,
        port=config.DataBase.db_port,
    )
    bot = Bot(
        token=config.TgBot.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher(storage=storage)

    # i18n = I18n(path="locales", default_locale="ru", domain="messages")
    # ConstI18nMiddleware(i18n=i18n, locale="ru").setup(dp)

    dp.include_routers(*routers_list)
    dp.include_routers(...)

    dp.update.outer_middleware(ConfigMiddleware(config))
    dp.update.outer_middleware(DbMiddleware(database))
    dp.update.outer_middleware(ErrorMiddleware())
    await bot.set_my_commands(
        [
            BotCommand(command="/start", description="Start"),
        ]
    )
    await database.create_tables()
    setup_dialogs(dp)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Bot turned off")
