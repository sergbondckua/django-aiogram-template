import logging

from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery)
from aiogram.utils.deep_linking import get_start_link
from aiogram import types
from aiogram.utils.markdown import text, hbold, quote_html, hcode
from asgiref.sync import sync_to_async

from loader import dp, _
from robot.models import TelegramUser
from robot.utils.weather import GisMeteoWeatherReport


@dp.message_handler(commands=["myid", "my_id"])
async def cmd_info_id(message: types.Message):
    """
    Return user ID information
    Повертає ID-інфо користувача
    """

    full_name = message.from_user.full_name
    userid = message.from_user.id
    chat_id = message.chat.id
    username = message.from_user.mention if message.from_user.mention else "➖"

    if types.ChatType.PRIVATE != message.chat.type:
        title = message.chat.title
    else:
        title = full_name

    msg = text(
        hbold(_("Your ID information:")),
        text("🚻", hbold(_("Full name:")), quote_html(full_name)),
        text("🪪", hbold(_("Username:")), quote_html(username)),
        text("🆔", hbold(_("Your ID:")), hcode(userid)),
        text("💬", hbold(_("Chat ID:")), hcode(chat_id)),
        text("🔸", hbold(_("Title:")), hcode(title)),
        sep="\n",
    )
    await types.ChatActions.typing()
    await message.answer(text=msg)


# хендлер для создания ссылок
@dp.message_handler(commands=["ref"])
async def get_ref(message: types.Message):
    link = await get_start_link("urlpay", encode=False)
    await message.answer(f"Ваша реф. ссылка {link}")


@dp.message_handler(commands="lang")
async def cmd_lang(message: types.Message):
    # Отдадим пользователю клавиатуру с выбором языков
    languages_markup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [
                InlineKeyboardButton(
                    text=_("English"), callback_data="lang_en"),
                InlineKeyboardButton(
                    text=_("Україньска"), callback_data="lang_uk"),
            ]
        ]
    )
    # For setting custom lang you have to modify i18n middleware
    await message.answer(
        _("Your current language:"), reply_markup=languages_markup)


@dp.callback_query_handler(text_contains="lang")
async def change_language(call: CallbackQuery):
    await call.message.edit_reply_markup()
    await call.message.delete()
    # Достаем последние 2 символа (например ru)
    lang = call.data[-2:]
    await TelegramUser.objects.filter(userid=call.from_user.id).aupdate(
        language_code=lang
    )
    # После того, как мы поменяли язык, в этой функции все еще указан старый, поэтому передаем locale=lang
    await call.message.answer(_("Your language has been changed", locale=lang))


@dp.message_handler(commands="weather")
async def cmd_weather(_: types.Message):
    """Command to weather"""
    if weather := await sync_to_async(
            GisMeteoWeatherReport().get_weather_forecast)():
        for chat_id, msg_forecast in weather.items():
            await dp.bot.send_message(chat_id=chat_id, text=msg_forecast)

    logging.info(
        "Weather information is not available to the request conditions")
