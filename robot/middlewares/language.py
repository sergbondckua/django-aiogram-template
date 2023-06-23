from aiogram import types
from aiogram.contrib.middlewares.i18n import I18nMiddleware
from django.conf import settings

from robot.models import TelegramUser


async def get_lang(userid):
    # Делаем запрос к базе, узнаем установленный язык
    try:
        user = await TelegramUser.objects.aget(userid=userid)
    except TelegramUser.DoesNotExist:
        return
    # Если пользователь найден - возвращаем его
    return user.language_code


class ACLMiddleware(I18nMiddleware):
    async def get_user_locale(self, action, args):
        """Every time you need to know the user's language"""
        user = types.User.get_current()
        # return the language from the database OR (if not found)
        # - language from Telegram
        return await get_lang(user.id) or user.locale


def setup_middleware(dp):
    """Setup i18n middleware"""
    i18n = ACLMiddleware("django", settings.LOCALES_DIR)
    dp.middleware.setup(i18n)
    return i18n
