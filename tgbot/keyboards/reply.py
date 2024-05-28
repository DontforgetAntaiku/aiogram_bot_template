from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.i18n import gettext as _


async def manager_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("Новая заметка")),
                KeyboardButton(text=_("Новая согласованная реклама")),
                KeyboardButton(text=_("Статистика")),
            ]
        ],
        resize_keyboard=True,
    )


async def author_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("Статистика")),
            ]
        ],
        resize_keyboard=True,
    )
