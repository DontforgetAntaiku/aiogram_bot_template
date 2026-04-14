from typing import Any, cast

from aiogram.types import TelegramObject
from aiogram.utils.i18n import I18nMiddleware
from babel.support import LazyProxy

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


def gettext(*args: Any, **kwargs: Any) -> str:
    from app.core import I18N

    return I18N.gettext(*args, **kwargs)


def lazy_gettext(*args: Any, **kwargs: Any) -> str:
    return cast(str, LazyProxy(gettext, *args, **kwargs, enable_cache=False))
