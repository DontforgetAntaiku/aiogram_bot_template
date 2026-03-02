from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.types import User as TelegramUser

from app.database.models import User


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        event_user: TelegramUser | None = data.get("event_from_user")
        if event_user is None:
            return await handler(event, data)

        user, _ = await User.update_or_create(
            defaults={
                "username": event_user.username,
                "first_name": event_user.first_name,
                "last_name": event_user.last_name,
            },
            id=event_user.id,
        )
        data["user"] = user
        return await handler(event, data)
