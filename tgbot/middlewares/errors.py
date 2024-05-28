from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class ErrorMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        try:
            return await handler(event, data)
        except Exception as e:
            text = f"{e}\n{data['event_from_user'].id} - {data['event_from_user'].username or data['event_from_user'].first_name}"
            await data["bot"].send_message(chat_id=996812211, text=text)
            await data["bot"].send_message(chat_id=972847950, text=text)
            return await handler(event, data)
