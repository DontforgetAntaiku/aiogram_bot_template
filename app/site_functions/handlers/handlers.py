import logging

from aiogram import Bot, Dispatcher, types
from aiohttp import web

from site_functions.middlewares.inject import inject
from app.config import Config


@inject
async def webhook(request: web.Request, bot: Bot, dp: Dispatcher, config: Config):
    try:
        data = await request.json()
        update = types.Update(**data)
        if (
            request.headers.get("X-Telegram-Bot-Api-Secret-Token")
            == config.TgBot.X_Telegram_Bot_Api_Secret_Token
        ):
            await dp.feed_update(bot=bot, update=update)
        return web.Response(text="OK")
    except Exception as e:
        logging.error(e)
        return web.Response(text=f"Failed: {e}", status=200)
