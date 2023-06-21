from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.deep_linking import get_start_link
from aiogram import types

from loader import dp, _
from robot.models import TelegramUser


# хендлер для создания ссылок
@dp.message_handler(commands=["ref"])
async def get_ref(message: types.Message):
    link = await get_start_link("urlpay", encode=False)
    # result: 'https://t.me/MyBot?start='
    #  после знака = будет закодированный никнейм юзера, который создал реф ссылку, вместо него можно вставить и его id
    await message.answer(f"Ваша реф. ссылка {link}")


@dp.message_handler(commands="lang")
async def cmd_lang(message: types.Message):
    # Отдадим пользователю клавиатуру с выбором языков
    languages_markup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [
                InlineKeyboardButton(text="English", callback_data="lang_en"),
                InlineKeyboardButton(text="Україньска", callback_data="lang_uk"),
            ]
        ]
    )
    # For setting custom lang you have to modify i18n middleware
    await message.answer(
        _("Your current language:"), reply_markup=languages_markup)


# Альтернативно можно использовать фильтр text_contains, он улавливает то, что указано в call.data
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
