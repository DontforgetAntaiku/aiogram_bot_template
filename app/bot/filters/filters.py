from aiogram.filters import BaseFilter
from aiogram.types import Message

from app.core import CONFIG


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.chat.id in CONFIG
