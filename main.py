import os

from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp.web import Application, run_app
from tortoise.contrib.aiohttp import register_tortoise

from app.bot.handlers import BOT_ROUTERS_LIST
from app.core import BOT, CONFIG, DISPATCHER, I18N, WORK_DIR
from app.database import TORTOISE_ORM
from app.utils.classes.services import Services
from app.utils.middlewares.site.inject import InjectMiddleware


def main():
    Services.setup_logging()

    os.chdir(WORK_DIR)
    app = Application(
        middlewares=(
            InjectMiddleware(config=CONFIG, bot=BOT, dp=DISPATCHER),  # pyright: ignore
        )
    )
    DISPATCHER.include_routers(*BOT_ROUTERS_LIST)
    Services.initialize_bot_middlewares(DISPATCHER, I18N)
    DISPATCHER.startup.register(Services.on_startup)
    DISPATCHER.shutdown.register(Services.on_shutdown)
    SimpleRequestHandler(
        dispatcher=DISPATCHER,
        bot=BOT,
        secret_token=CONFIG.webhook.X_Telegram_Bot_Api_Secret_Token,
    ).register(app, CONFIG.webhook.PATH)
    setup_application(app, DISPATCHER, bot=BOT, config=CONFIG)
    register_tortoise(app, TORTOISE_ORM, generate_schemas=True)
    run_app(app, host=CONFIG.webhook.HOST, port=CONFIG.webhook.PORT)


if __name__ == "__main__":
    main()
