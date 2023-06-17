import logging
import asyncio
from datetime import datetime

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentTypes, ReplyKeyboardRemove
from aiogram.dispatcher.filters.builtin import CommandStart, Text
from aiogram.utils.deep_linking import decode_payload
from asgiref.sync import sync_to_async

from django.db import IntegrityError

from loader import dp
import const_texts as ct

from robot.keyboards.default import make_buttons, contact_request_button
from robot.states.user_register import UserChatRegister
from robot.models import TelegramUser


#  Cancellation of data entry
@dp.message_handler(
    Text(equals=ct.c_cancel, ignore_case=True), state=UserChatRegister)
async def cancel_data_entry(message: Message, state: FSMContext):
    await message.answer(
        text=ct.c_cancel_msg, reply_markup=ReplyKeyboardRemove())
    await state.reset_state()


@dp.message_handler(CommandStart())
async def cmd_start(message: Message):
    if args := message.get_args():
        reference = decode_payload(args)
        await message.answer(f"Ваш реферер {reference}")
        await asyncio.sleep(3)

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
    if not (telegram_user.phone and telegram_user.birthday):
        await UserChatRegister.yes_or_no.set()
        await message.answer(
            text=ct.c_get_hello(message.from_user.first_name),
            reply_markup=make_buttons([ct.c_yes, ct.c_cancel], row_width=2),
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



#  If the consent button was clicked
@dp.message_handler(
    Text(equals=ct.c_yes, ignore_case=True), state=UserChatRegister.yes_or_no)
async def approved(message: Message):
    await UserChatRegister.next()
    await message.answer(
        text=ct.c_input_phone_number, reply_markup=contact_request_button)


@dp.message_handler(
    state=UserChatRegister.phone, content_types=ContentTypes.CONTACT)
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
    first_name = user_info.get("first_name")
    last_name = user_info.get("last_name")
    phone = user_info.get("phone")

    try:
        await TelegramUser.objects.filter(
            userid=message.from_user.id).aupdate(
            phone=phone,
            first_name=first_name,
            last_name=last_name,
            birthday=birth_date
        )
        avatar = await message.from_user.get_profile_photos(offset=-1, limit=1)
        if avatar.total_count:
            await message.answer_photo(
                photo=avatar.photos[0][-1].file_id,
                caption=f"{first_name} {last_name} \n📱 {phone} \n"
                        f"🎂 {birth_date.strftime('%d.%m.%Y')} \n"
            )
        else:
            await message.answer(
                text=f"{first_name} {last_name} \n{phone} \n"
                     f"{birth_date.strftime('%d.%m.%Y')} \n"
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


#  If the date format is incorrect
@dp.message_handler(state=UserChatRegister.birthday)
async def not_valid_birth_date(message: Message):
    await message.answer(
        text=ct.c_input_birthday_again)


#  If a message is sent without a contact
@dp.message_handler(
    lambda message: not message.contact, state=UserChatRegister.phone)
async def check_contact(message: Message):
    await message.reply(
        text=ct.c_share_phone_number_not_valid,
        reply_markup=contact_request_button
    )


#  If the consent or cancel button is not pressed
@dp.message_handler(state=UserChatRegister.yes_or_no)
async def not_approved(message: Message):
    await message.answer(
        text=ct.c_take_approval,
        reply_markup=make_buttons(words=[ct.c_yes, ct.c_cancel], row_width=2)
    )
