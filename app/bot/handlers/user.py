from aiogram import Router, filters, types
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

user_router = Router()


@user_router.message(filters.CommandStart())
async def user_start(message: types.Message):
    await message.answer(_("welcome_text"))
