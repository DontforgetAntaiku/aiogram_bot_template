import logging

import betterlogging as bl
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from aiogram.types import BotCommand
from aiohttp import web
from redis.asyncio import Redis

from app.config import Config
from app.db.database import DB
from app.middlewares.config import ConfigMiddleware
from app.middlewares.errors import ErrorMiddleware
from app.services.classes import SingletonFactory
from app.site_functions.handlers.handlers import webhook


class Services(SingletonFactory):
    def get_bot(config: Config):
        bot = Bot(
            token=config.TgBot.BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )
        return bot

    def get_database(config: Config):
        database = DB(
            user=config.DataBase.DB_USER,
            password=config.DataBase.DB_PASSWORD,
            dbname=config.DataBase.DB_NAME,
            host=config.DataBase.DB_HOST,
            port=config.DataBase.DB_PORT,
        )
        return database

    def get_redis(config: Config):
        redis = Redis(host=config.TgBot.REDIS_HOST, port=config.TgBot.REDIS_PORT)
        return redis

    def get_storage(redis: Redis):
        storage = RedisStorage(redis, key_builder=DefaultKeyBuilder(with_destiny=True))
        return storage

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

    def initialize_bot_middlewares(dp: Dispatcher, config: Config):
        dp.update.outer_middleware(ConfigMiddleware(config))
        dp.update.outer_middleware(ErrorMiddleware())

    async def on_startup(bot: Bot, config: Config) -> None:
        print(f"https://t.me/{(await bot.get_me()).username}")
        await bot.set_webhook(
            f"{config.Webhook.BASE_URL}{config.Webhook.WEBHOOK_PATH}",
            secret_token=config.Webhook.X_Telegram_Bot_Api_Secret_Token,
            allowed_updates=[],
        )

    async def set_admin_commands(bot: Bot, config: Config):
        await bot.set_my_commands(
            [
                BotCommand(command="/start", description="Start"),
            ]
        )

    def setup_aiogram_dialogs(dp):
        from aiogram_dialog import setup_dialogs

        dp.include_routers()
        setup_dialogs(dp)

    async def on_shutdown(bot: Bot):
        await bot.delete_webhook(drop_pending_updates=True)

    def add_routes(app: web.Application, config: Config):
        app.router.add_post(config.Webhook.WEBHOOK_PATH, webhook)
