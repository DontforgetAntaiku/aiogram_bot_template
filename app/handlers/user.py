from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.database.models import User

user_router = Router()


@user_router.message(CommandStart())
async def user_start(message: Message):
    user = await User.update_or_create(
        id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
    )
    user
    await message.answer(message.html_text)
