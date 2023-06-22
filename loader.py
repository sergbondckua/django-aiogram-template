from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.i18n import I18nMiddleware
from django.conf import settings

from robot.models import TelegramUser

bot = Bot(token=settings.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def get_lang(userid):
    # Делаем запрос к базе, узнаем установленный язык
    try:
        user = await TelegramUser.objects.aget(userid=userid)
    except TelegramUser.DoesNotExist:
        return
    # Если пользователь найден - возвращаем его
    return user.language_code


class ACLMiddleware(I18nMiddleware):
    # Каждый раз, когда нужно узнать язык пользователя - выполняется эта функция
    async def get_user_locale(self, action, args):
        user = types.User.get_current()
        # Возвращаем язык из базы ИЛИ (если не найден) - язык из Телеграма
        return await get_lang(user.id) or user.locale


# Alias for gettext method
i18n = ACLMiddleware("django", settings.LOCALES_DIR)
dp.middleware.setup(i18n)
_ = i18n.gettext
