import logging
from datetime import datetime

from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.dispatcher.filters.builtin import CommandStart
from asgiref.sync import sync_to_async

from django.db import IntegrityError

from loader import dp
import const_texts as ct
from robot.keyboards.default import make_buttons, contact_request_button
from robot.states.user_register import UserChatRegister
from robot.models import TelegramUser


@dp.message_handler(text_contains="cancel", state=UserChatRegister)
async def approval(message: Message, state: FSMContext):
    await message.edit_reply_markup()  # Remove buttons
    await message.answer("Ви скасували реєстрацію")
    await state.reset_state()


@dp.message_handler(CommandStart())
async def cmd_start(message: Message):
    telegram_user, _ = await TelegramUser.objects.aget_or_create(
        userid=message.from_user.id,
        defaults={
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
            "language_code": message.from_user.locale.language,
        }

    )

    user = await sync_to_async(telegram_user.get_user)()
    if user is not None:
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
            text=ct.c_get_hello(message.from_user.full_name),
            reply_markup=make_buttons([ct.c_register]),
        )

    if telegram_user.phone is None:
        await UserChatRegister.phone.set()
        await message.answer(
            text=ct.c_input_phone_number, reply_markup=contact_request_button
        )


@dp.message_handler(state=UserChatRegister.phone, content_types="contact")
async def register_phone(message: Message, state: FSMContext):
    #  Verification phone number belongs to this account
    if message.contact.user_id != message.from_user.id:
        await message.answer(text=ct.c_share_phone_number_again)
        return

    phone_number = message.contact.phone_number
    if not phone_number.startswith("+"):
        phone_number = "+" + phone_number

    await state.update_data(phone=phone_number)

    await UserChatRegister.next()
    await message.reply(
        text=ct.c_share_phone_number_thx(message.from_user.first_name))
    await message.answer(
        text=ct.c_input_first_name,
        reply_markup=make_buttons(
            words=[message.from_user.first_name, ct.c_cancel]),
    )


@dp.message_handler(state=UserChatRegister.first_name)
async def register_first_name(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await UserChatRegister.next()
    await message.answer(
        text=ct.c_input_last_name,
        reply_markup=make_buttons(
            words=[message.from_user.last_name, ct.c_cancel]),
    )


@dp.message_handler(state=UserChatRegister.last_name)
async def register_last_name(message: Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    await UserChatRegister.next()
    await message.answer(
        text=ct.c_input_birthday, reply_markup=make_buttons(
            words=[ct.c_cancel])
    )


@dp.message_handler(
    state=UserChatRegister.birthday, regexp=r"^\d{2}\.\d{2}\.\d{4}$")
async def register_birthday(message: Message, state: FSMContext):
    try:
        birth_date = datetime.strptime(message.text, "%d.%m.%Y")
    except ValueError:
        await message.answer(ct.c_input_birthday_incorrect)
        return

    user_info = await state.get_data()

    try:
        await TelegramUser.objects.filter(
            userid=message.from_user.id).aupdate(
            phone=user_info.get("phone"),
            first_name=user_info.get("first_name"),
            last_name=user_info.get("last_name"),
            birthday=birth_date
        )

        await message.answer(
            text=ct.c_successfully_register, reply_markup=make_buttons(
                [ct.c_about_us])
        )
    except IntegrityError:
        await message.answer(
            text=ct.c_registration_failed, reply_markup=make_buttons(
                [ct.c_register])
        )

    logging.info("%s user was successfully created", message.from_user.id)
    await message.delete()
    await state.finish()


@dp.message_handler(state=UserChatRegister.birthday)
async def not_valid_birth_date(message: Message):
    await message.answer(
        text=ct.c_input_birthday_again)
