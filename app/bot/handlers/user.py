from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.database.models import User

user_router = Router()


@user_router.message(CommandStart())
async def user_start(message: Message):
    if message.from_user is None:
        return
    await User.update_or_create(
        defaults=dict(
            id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
        ),
        id=message.from_user.id,
    )
    await message.answer(message.html_text)
