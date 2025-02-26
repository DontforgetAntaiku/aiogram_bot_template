from aiogram.filters import BaseFilter
from aiogram.types import Message

from app.config import Config


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message, config: Config) -> bool:
        return message.chat.id in config
