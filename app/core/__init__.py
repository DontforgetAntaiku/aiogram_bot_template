import logging
import os
from typing import Final

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.utils.i18n import I18n

from app.utils.classes.config import Config
from app.utils.classes.services import Services

LOG_LEVEL: Final[int] = logging.INFO

WORK_DIR: Final[str] = os.path.dirname(__file__)

CONFIG: Final = Config(".env")
REDIS = Services.get_redis(CONFIG)
REDIS_STORAGE = Services.get_storage(REDIS)
BOT = Bot(
    token=CONFIG.bot.TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
DISPATCHER = Dispatcher(
    storage=REDIS_STORAGE,
)
I18N = I18n(path="locales")
try:
    from aiogram_dialog import BgManagerFactory, setup_dialogs

    BG_FACTORY: BgManagerFactory = setup_dialogs(DISPATCHER)
except ModuleNotFoundError:
    logging.info("aiogram_dialog is not installed")
