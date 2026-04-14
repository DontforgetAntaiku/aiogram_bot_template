from collections.abc import Callable

from aiogram.types import (
    KeyboardButton,
    KeyboardButtonRequestChat,
    KeyboardButtonRequestUser,
    KeyboardButtonRequestUsers,
)
from aiogram_dialog.api.internal import RawKeyboard, StyleWidget, TextWidget
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.kbd import Keyboard
from aiogram_dialog.widgets.style import EMPTY_STYLE

KeyboardButtonRequest = (
    KeyboardButtonRequestUser | KeyboardButtonRequestUsers | KeyboardButtonRequestChat
)


class CustomRequest(Keyboard):
    """Reply keyboard only"""

    def __init__(
        self,
        text: TextWidget,
        button_request: KeyboardButtonRequest,
        when: str | Callable | None = None,
        style: StyleWidget = EMPTY_STYLE,
    ):
        super().__init__(when=when)
        self.text = text
        self.button_request = button_request
        self.style = style

    async def _render_keyboard(
        self,
        data: dict,
        manager: DialogManager,
    ) -> RawKeyboard:
        style = await self.style.render_style(data, manager)
        icon_custom_emoji_id = await self.style.render_emoji(data, manager)
        match self.button_request:
            case KeyboardButtonRequestUsers():
                return [
                    [
                        KeyboardButton(
                            text=await self.text.render_text(data, manager),
                            style=style,
                            icon_custom_emoji_id=icon_custom_emoji_id,
                            request_users=self.button_request,
                        )
                    ]
                ]
            case KeyboardButtonRequestUser():
                return [
                    [
                        KeyboardButton(
                            text=await self.text.render_text(data, manager),
                            style=style,
                            icon_custom_emoji_id=icon_custom_emoji_id,
                            request_uesr=self.button_request,
                        )
                    ]
                ]
            case KeyboardButtonRequestChat():
                return [
                    [
                        KeyboardButton(
                            text=await self.text.render_text(data, manager),
                            style=style,
                            icon_custom_emoji_id=icon_custom_emoji_id,
                            request_chat=self.button_request,
                        )
                    ]
                ]
