from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from tgbot.db.database import DB


class DbMiddleware(BaseMiddleware):
    def __init__(self, db: DB):
        super().__init__()
        self.db = DB

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        async with self.db.get_session() as session:
            data["db_session"] = session
            return await handler(event, data)