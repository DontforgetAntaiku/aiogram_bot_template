from aiogram.filters import BaseFilter
from aiogram.types import Message

from app.classes.singleton import SingletonFactory
from app.config import load_config


class IsAdmin(SingletonFactory, BaseFilter):
    def init(self, *args, **kwargs):
        self.admins_id = load_config().tg_bot.admins_id

    async def __call__(self, message: Message) -> bool:
        return message.chat.id in self.admins_id
