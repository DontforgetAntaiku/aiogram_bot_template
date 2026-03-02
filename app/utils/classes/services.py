import logging

import betterlogging as bl
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import BotCommand
from aiohttp import web
from redis.asyncio import Redis

from app.site.routers.main.view import webhook
from app.utils.classes.config import Config
from app.utils.middlewares.bot.errors import ErrorMiddleware


class Services:
    @staticmethod
    def get_redis(config: Config):
        redis = Redis(host=config.redis.HOST, port=config.redis.PORT)
        return redis

    @staticmethod
    def get_storage(redis: Redis):
        storage = RedisStorage(redis, key_builder=DefaultKeyBuilder(with_destiny=True))
        return storage

    @staticmethod
    def setup_logging():
        from app.core import LOG_LEVEL

        log_level = LOG_LEVEL
        bl.basic_colorized_config(style="%", level=log_level)
        logging.info("Starting bot")

    @staticmethod
    def initialize_bot_middlewares(dp: Dispatcher, config: Config):
        dp.update.outer_middleware(ErrorMiddleware())

    @staticmethod
    async def on_startup(bot: Bot, config: Config) -> None:
        print(f"https://t.me/{(await bot.get_me()).username}")
        await bot.set_webhook(
            f"{config.webhook.BASE_URL}{config.webhook.PATH}",
            secret_token=config.webhook.X_Telegram_Bot_Api_Secret_Token,
            allowed_updates=[],
        )

    @staticmethod
    async def set_admin_commands(bot: Bot, config: Config):
        await bot.set_my_commands(
            [
                BotCommand(command="/start", description="Start"),
            ]
        )

    @staticmethod
    def setup_aiogram_dialogs(dp: Dispatcher):

        dp.include_routers()

    @staticmethod
    async def on_shutdown(bot: Bot):
        await bot.delete_webhook(drop_pending_updates=True)

    @staticmethod
    def add_routes(app: web.Application, config: Config):
        app.router.add_post(config.webhook.PATH, webhook)
