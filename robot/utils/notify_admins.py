import logging

from aiogram import Dispatcher

from django.utils.translation import gettext_lazy as _

from robot.models import TelegramUser
from robot.middlewares import *
from robot.handlers import *


async def on_startup_notify(dp: Dispatcher):
    async for admin in TelegramUser.objects.filter(is_admin=True):
        name_bot = await dp.bot.get_me()
        try:
            await dp.bot.send_message(
                admin.userid,
                _("🖥 Запущено - Бот: ") +
                f"<code>{name_bot.first_name} [@{name_bot.username}]</code>"
            )

        except Exception as err:
            logging.exception(err)
