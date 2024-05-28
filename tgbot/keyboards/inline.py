from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _


async def accept_button(ad_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=_("Принять"), callback_data=f"accept:{ad_id}")]
        ]
    )


async def send_link_button(ad_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=_("Отправить ссылку"), callback_data=f"send_link:{ad_id}"
                )
            ]
        ]
    )


async def admin_pay_keyboard(
    ad_id, var, wallet=None, amount=None, wallet_type=None, username=None
):
    if var == 1:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Принять", callback_data=f"admin_accept:{ad_id}"
                    )
                ]
            ]
        )
    elif var == 2:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=f"Принято @{username}",
                        callback_data="_",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="Оплатить",
                        url=f"https://app.tonkeeper.com/transfer/{wallet}?amount={int((amount*pow(10, 9)))}"
                        if wallet_type == "TON"
                        else f"https://link.trustwallet.com/send?asset=c195_tTR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t&address={wallet}&amount={amount}",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="Подтвердить оплату", callback_data=f"confirm:{ad_id}"
                    ),
                ],
            ]
        )
    elif var == 3:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=f"Заявка обработана @{username}", callback_data="_"
                    )
                ]
            ]
        )
