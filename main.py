import asyncio
import logging
import os

from aiogram import Dispatcher
from aiogram.webhook.aiohttp_server import setup_application
from aiohttp import web

from app.config import Config
from app.handlers import routers_list
from app.services.services import Services
from app.site_functions.middlewares.inject import InjectMiddleware


def main():
    os.chdir(os.path.dirname(__file__))
    config = Config(".env")
    Services.setup_logging()
    redis = Services.get_redis(config)
    storage = Services.get_storage(redis)
    bot = Services.get_bot(config)
    database = Services.get_database(config)
    dp = Dispatcher(storage=storage)
    app = web.Application(
        middlewares=[
            InjectMiddleware(config=config, bot=bot, dp=dp),
        ]
    )

    dp.include_routers(*routers_list)
    Services.initialize_bot_middlewares(dp, config)
    Services.add_routes(app, config)
    dp.startup.register(Services.on_startup)
    dp.shutdown.register(Services.on_shutdown)
    setup_application(app, dp, bot=bot, database=database)

    web.run_app(
        app, host=config.Webhook.WEB_SERVER_HOST, port=config.Webhook.WEB_SERVER_PORT
    )


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        logging.error("Bot turned off")
