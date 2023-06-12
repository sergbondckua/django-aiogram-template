import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db.utils import IntegrityError
from asgiref.sync import sync_to_async

from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from loader import dp
import const_texts as ct

from robot.models import TelegramUser
from robot.states import UserRegister
from robot.keyboards.default import make_buttons, contact_request_button


@dp.message_handler(text=ct.c_register)
async def register(message: Message):
    await UserRegister.username.set()
    await message.answer(
        text=ct.c_input_phone_number, reply_markup=contact_request_button
    )


@dp.message_handler(state=UserRegister.username, content_types="contact")
async def register(message: Message, state: FSMContext):

    #  Verification phone number belongs to this account
    if message.contact.user_id != message.from_user.id:
        await message.answer(text="This is not your phone number. Try again.")
        return

    phone_number = message.contact.phone_number
    if not phone_number.startswith("+"):
        phone_number = "+" + phone_number

    user = await get_user_model().objects.filter(
        username=phone_number).afirst()
    if user:
        telegram_user = await TelegramUser.objects.aget(
            userid=message.from_user.id)
        await sync_to_async(telegram_user.set_user)(user)
        await message.answer(
            text=ct.c_successfully_register, reply_markup=make_buttons(
                [ct.c_about_us])
        )
        logging.info("%s user was successfully connected", user.username)
        await state.finish()
        return

    await UserRegister.next()
    await message.answer(
        text=ct.c_input_first_name,
        reply_markup=make_buttons(
            words=[message.from_user.first_name, ct.c_cancel]),
    )

    await state.update_data(username=phone_number, phone=phone_number)


@dp.message_handler(state=UserRegister.first_name)
async def register(message: Message, state: FSMContext):
    await UserRegister.next()
    await message.answer(
        text=ct.c_input_last_name,
        reply_markup=make_buttons(
            words=[message.from_user.last_name, ct.c_cancel]),
    )
    await state.update_data(first_name=message.text)


@dp.message_handler(state=UserRegister.last_name)
async def register(message: Message, state: FSMContext):
    await UserRegister.next()
    await message.answer(
        text=ct.c_input_password, reply_markup=make_buttons(
            words=[ct.c_cancel])
    )
    await state.update_data(last_name=message.text)


@dp.message_handler(
    state=UserRegister.password,
    regexp=r"^(?=.*[0-9].*)(?=.*[a-z].*)(?=.*[A-Z].*)[0-9a-zA-Z]{8,}$")
async def register(message: Message, state: FSMContext):
    user_info = await state.get_data()

    try:
        user = await get_user_model().objects.acreate(
            username=user_info.get("username"),
            first_name=user_info.get("first_name"),
            last_name=user_info.get("last_name"),
            password=make_password(message.text),
        )
        telegram_user = await TelegramUser.objects.aget(
            userid=message.from_user.id)
        telegram_user.phone = user_info.get("phone")
        await sync_to_async(telegram_user.save)()
        await sync_to_async(telegram_user.set_user)(user)

        await message.answer(
            text=ct.c_successfully_register, reply_markup=make_buttons(
                [ct.c_about_us])
        )
    except IntegrityError:
        await message.answer(
            text=ct.c_registration_failed, reply_markup=make_buttons(
                [ct.c_register])
        )

    await message.delete()
    await state.finish()

    logging.info("%s user was successfully created", user.username)


# Called if the password has not validated
@dp.message_handler(state=UserRegister.password)
async def not_valid_password(message: Message):
    await message.answer(
        text=ct.c_input_password_again)
