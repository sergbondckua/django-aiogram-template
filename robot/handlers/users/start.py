import logging
import asyncio

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher.filters.builtin import CommandStart
from asgiref.sync import sync_to_async


from loader import dp, _
import const_texts as ct

from robot.keyboards.default import make_buttons
from robot.states.user_register import UserChatRegister
from robot.models import TelegramUser
from robot.utils.misc.deeplink_process import get_deeplink


@dp.message_handler(
    lambda message: message.text == _(ct.c_cancel), state="*")
async def cancel_data_entry(message: Message, state: FSMContext):
    """ Cancel data entry from Telegram user """

    await message.answer(
        text=_(ct.c_cancel_msg), reply_markup=ReplyKeyboardRemove())
    await state.reset_state()
    logging.info(
        "User %s (%s) has canceled the entry of personal data",
        message.from_user.first_name, message.from_user.id)


@dp.message_handler(CommandStart())
async def cmd_start(message: Message):
    """ Start command processing """

    #  If the start command was used with an argument `/start arg` (deeplink)
    if args := message.get_args():
        await get_deeplink(link=args, tg_object=message)
        await asyncio.sleep(3)

    #  Get or create (if there is none) a user in the database
    telegram_user, _ = await TelegramUser.objects.aget_or_create(
        userid=message.from_user.id,
        defaults={
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
            "language_code": message.from_user.locale.language,
        }

    )

    #  Get the site user associated with the Telegram user
    user = await sync_to_async(telegram_user.get_user)()

    #  If the corresponding fields in the DB are not filled,
    #  make a request for registration
    if not (telegram_user.phone and telegram_user.birthday):
        logging.info("User %s (%s) with incomplete information about him",
                     message.from_user.first_name, message.from_user.id)
        await UserChatRegister.yes_or_no.set()
        await message.answer(
            text=ct.c_get_hello(message.from_user.first_name),
            reply_markup=make_buttons(
                words=[ct.c_yes, ct.c_cancel], row_width=2),
        )
    elif user is not None:
        logging.info("User already exists")
        await message.answer(
            text=ct.c_get_hello_back(
                user.first_name,
                user.last_name,
            ),
            reply_markup=make_buttons([ct.c_about_us]),
        )
    else:
        logging.info("New user")
        await message.answer(
            text=ct.c_get_hello(message.from_user.first_name),
            reply_markup=make_buttons([ct.c_register]),
        )
