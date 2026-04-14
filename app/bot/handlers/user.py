from aiogram import Router, filters, types

from app.utils.middlewares.bot.i18n import gettext as _

router = Router(name="User router")


@router.message(filters.CommandStart())
async def user_start(message: types.Message):
    await message.answer(_("welcome_text"))
