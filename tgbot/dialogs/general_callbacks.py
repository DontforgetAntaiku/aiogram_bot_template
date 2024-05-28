from aiogram.types import Message
from aiogram.utils.i18n import gettext as _
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput


async def incorrect_type_user(
    message: Message,
    message_input: MessageInput,
    dialog_manager: DialogManager,
):
    dialog_manager.show_mode = ShowMode.DELETE_AND_SEND
    await message.answer(_("<b>Неправильный формат!</b>\n\n" "Попробуйте ещё раз... ⚠️"))


async def error_zero(callback_query, button, dialog_manager: DialogManager):
    dialog_manager.start_data["error"] = ""
    dialog_manager.dialog_data["error"] = ""


async def incorrect_type(
    message: Message,
    message_input: MessageInput,
    dialog_manager: DialogManager,
):
    dialog_manager.show_mode = ShowMode.DELETE_AND_SEND
    await message.answer(("<b>Неправильный формат!</b>\n\n" "Попробуйте ещё раз... ⚠️"))


async def cancel_dialog(callback_query, button, dialog_manager: DialogManager):
    await dialog_manager.done()
    await callback_query.message.delete()
