import logging

from aiogram import Dispatcher

from aiogram.utils.markdown import text, hcode
from django.utils.translation import gettext_lazy as _

from robot.middlewares import *
from robot.handlers import *
from robot.utils.service import send_message_to_bot_admins


async def on_startup_notify(dp: Dispatcher):
    name_bot = await dp.bot.get_me()
    msg = text(
        _("🖥 Запущено - Бот: "),
        text(hcode(name_bot.first_name), "@" + name_bot.username),
    )
    try:
        await send_message_to_bot_admins(msg)
    except Exception as err:
        logging.exception(err)
