import os

from aiogram.webhook.aiohttp_server import setup_application
from aiohttp import web
from tortoise.contrib.aiohttp import register_tortoise

from app.bot.handlers import BOT_ROUTERS_LIST
from app.core import BOT, CONFIG, DISPATCHER, WORK_DIR
from app.database import TORTOISE_ORM
from app.utils.classes import Services
from app.utils.middlewares.site.inject import InjectMiddleware


def main():
    Services.setup_logging()

    os.chdir(WORK_DIR)
    app = web.Application(
        middlewares=[
            InjectMiddleware(config=CONFIG, bot=BOT, dp=DISPATCHER),
        ]
    )
    DISPATCHER.include_routers(*BOT_ROUTERS_LIST)
    Services.initialize_bot_middlewares(DISPATCHER, CONFIG)
    DISPATCHER.startup.register(Services.on_startup)
    DISPATCHER.shutdown.register(Services.on_shutdown)
    setup_application(app, DISPATCHER, bot=BOT, config=CONFIG)
    Services.add_routes(app, CONFIG)
    register_tortoise(app, TORTOISE_ORM, generate_schemas=True)

    web.run_app(app, host=CONFIG.webhook.HOST, port=CONFIG.webhook.PORT)


if __name__ == "__main__":
    main()
