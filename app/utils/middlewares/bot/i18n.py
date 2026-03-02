from typing import Any

from aiogram.types import TelegramObject
from aiogram.utils.i18n import I18nMiddleware

DEFAULT_LOCALE = "ru"


class I18NMiddleware(I18nMiddleware):
    async def get_locale(
        self,
        event: TelegramObject,
        data: dict[str, Any],
    ) -> str:
        from app.core import I18N

        user = data.get("event_from_user")
        if user and user.language_code in I18N.available_locales:
            return user.language_code
        return DEFAULT_LOCALE
