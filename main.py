import asyncio
import logging

import betterlogging as bl
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import DefaultKeyBuilder, Redis, RedisStorage
from aiogram.types import BotCommand
# from aiogram.utils.i18n import ConstI18nMiddleware, I18n
from aiogram_dialog import setup_dialogs

from tgbot.config import load_config
from tgbot.db.database import MyDb
from tgbot.handlers import routers_list
from tgbot.middlewares.config import ConfigMiddleware
from tgbot.middlewares.db import DbMiddleware
from tgbot.middlewares.errors import ErrorMiddleware


def setup_logging():
    log_level = logging.ERROR

    # Initialize betterlogging for colorized console output
    bl.basic_colorized_config(level=logging.INFO)

    # Create a logger
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    # Remove any existing handlers to prevent duplicate logs
    if logger.hasHandlers():
        logger.handlers.clear()

    # Create a file handler
    file_handler = logging.FileHandler(r"logging.txt")
    file_handler.setLevel(log_level)
    file_formatter = logging.Formatter(
        "%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s"
    )
    file_handler.setFormatter(file_formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    # Console handler is already set up by betterlogging
    # Add the logger to the root to catch all logs from all modules
    logging.getLogger().addHandler(file_handler)

    logging.error("Starting bot")


async def main():
    config = load_config(".env")
    setup_logging()
    redis = Redis(host=config.tg_bot.redis_host, port=config.tg_bot.redis_port)
    storage = RedisStorage(redis, key_builder=DefaultKeyBuilder(with_destiny=True))

    bot = Bot(token=config.tg_bot.token, parse_mode=ParseMode.HTML)

    dp = Dispatcher(storage=storage)

    # i18n = I18n(path="locales", default_locale="ru", domain="messages")
    # ConstI18nMiddleware(i18n=i18n, locale="ru").setup(dp)


    dp.include_routers(*routers_list)
    dp.include_routers(...)

    dp.update.outer_middleware(ConfigMiddleware(config))
    dp.update.outer_middleware(DbMiddleware())
    dp.update.outer_middleware(ErrorMiddleware())
    await bot.set_my_commands(
        [
            BotCommand(command="/start", description="Start"),
        ]
    )
    await MyDb().db_setup()
    setup_dialogs(dp)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Bot turned off")
