import logging

from asgiref.sync import sync_to_async
from robot.models import TelegramUser

from aiogram.types import Message
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from const_texts import c_get_hello, c_get_hello_back, c_register, c_about_us
from robot.keyboards.default import make_buttons


@dp.message_handler(CommandStart())
async def bot_start(message: Message):
    username = message.from_user.username or None

    telegram_user, _ = await TelegramUser.objects.aget_or_create(
        userid=message.from_user.id,
        defaults=dict(
            username=username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            language_code=message.from_user.locale.language,
        )

    )
    user = await sync_to_async(telegram_user.get_user)()
    if user is not None:
        logging.info("User already exists")
        await message.answer(
            text=c_get_hello_back(
                user.first_name,
                user.last_name,
            ),
            reply_markup=make_buttons([c_about_us]),
        )
    else:
        logging.info("New user")
        await message.answer(
            text=c_get_hello(message.from_user.full_name),
            reply_markup=make_buttons([c_register]),
        )
