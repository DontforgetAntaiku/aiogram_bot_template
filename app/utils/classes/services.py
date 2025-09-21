import logging

import betterlogging as bl
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from aiogram.types import BotCommand
from aiohttp import web
from redis.asyncio import Redis

from app.site.routers.main.view import webhook
from app.utils.classes.config import Config
from app.utils.middlewares.bot.errors import ErrorMiddleware


class Services:
    def get_redis(config: Config):
        redis = Redis(host=config.redis.HOST, port=config.redis.PORT)
        return redis

    def get_storage(redis: Redis):
        storage = RedisStorage(redis, key_builder=DefaultKeyBuilder(with_destiny=True))
        return storage

    def setup_logging():
        log_level = logging.ERROR
        log_format = (
            "[%(asctime)s] %(levelname)s:(%(filename)s): %(lineno)d:%(message)s"
        )
        bl.basic_colorized_config(format=log_format, style="%", level=log_level)
        # logger = logging.getLogger(__name__)
        # logger.setLevel(log_level)
        # if logger.hasHandlers():
        #     logger.handlers.clear()
        # file_handler = logging.FileHandler(r"logging.txt")
        # file_handler.setLevel(log_level)
        # file_formatter = logging.Formatter(log_format)
        # file_handler.setFormatter(file_formatter)
        # logger.addHandler(file_handler)
        # logging.getLogger().addHandler(file_handler)
        logging.error("Starting bot")

    def initialize_bot_middlewares(dp: Dispatcher, config: Config):
        dp.update.outer_middleware(ErrorMiddleware())

    async def on_startup(bot: Bot, config: Config) -> None:
        print(f"https://t.me/{(await bot.get_me()).username}")
        await bot.set_webhook(
            f"{config.webhook.BASE_URL}{config.webhook.PATH}",
            secret_token=config.webhook.X_Telegram_Bot_Api_Secret_Token,
            allowed_updates=[],
        )

    async def set_admin_commands(bot: Bot, config: Config):
        await bot.set_my_commands(
            [
                BotCommand(command="/start", description="Start"),
            ]
        )

    def setup_aiogram_dialogs(dp: Dispatcher):
        from aiogram_dialog import setup_dialogs

        dp.include_routers()
        setup_dialogs(dp)

    async def on_shutdown(bot: Bot):
        await bot.delete_webhook(drop_pending_updates=True)

    def add_routes(app: web.Application, config: Config):
        app.router.add_post(config.webhook.PATH, webhook)
