import logging
from datetime import datetime

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentTypes
from django.db import IntegrityError

from loader import dp, _
import const_texts as ct
from robot.keyboards.default import get_contact_keyboard, make_buttons
from robot.models import TelegramUser
from robot.states import UserChatRegister


@dp.message_handler(lambda message: message.text == _(ct.c_yes),
                    state=UserChatRegister.yes_or_no)
async def approved(message: Message):
    """ If consent is obtained for maintaining personal data """

    await UserChatRegister.next()
    await message.answer(
        text=_(ct.c_input_phone_number), reply_markup=get_contact_keyboard())


@dp.message_handler(
    state=UserChatRegister.phone, content_types=ContentTypes.CONTACT)
async def register_phone(message: Message, state: FSMContext):
    """ Get the phone number """

    #  Verification phone number belongs to this account
    if message.contact.user_id != message.from_user.id:
        await message.answer(text=_(ct.c_share_phone_number_again))
        return

    phone_number = message.contact.phone_number
    if not phone_number.startswith("+"):
        phone_number = "+" + phone_number

    await state.update_data(phone=phone_number)

    await UserChatRegister.next()
    await message.reply(
        text=ct.c_share_phone_number_thx(message.from_user.first_name))
    await message.answer(
        text=_(ct.c_input_first_name),
        reply_markup=make_buttons(
            words=[message.from_user.first_name, ct.c_cancel]),
    )


@dp.message_handler(state=UserChatRegister.first_name)
async def register_first_name(message: Message, state: FSMContext):
    """ Get the first name of the user """

    await state.update_data(first_name=message.text)
    await UserChatRegister.next()
    await message.answer(
        text=_(ct.c_input_last_name),
        reply_markup=make_buttons(
            words=[message.from_user.last_name, ct.c_cancel]),
    )


@dp.message_handler(state=UserChatRegister.last_name)
async def register_last_name(message: Message, state: FSMContext):
    """ Get the last name of the user """

    await state.update_data(last_name=message.text)
    await UserChatRegister.next()
    await message.answer(
        text=_(ct.c_input_birthday), reply_markup=make_buttons(
            words=[ct.c_cancel])
    )


@dp.message_handler(
    state=UserChatRegister.birthday, regexp=r"^\d{2}\.\d{2}\.\d{4}$")
async def register_birthday(message: Message, state: FSMContext):
    """ Get the birthday of the user """

    #  Check for the correctness and existence of the date
    try:
        birth_date = datetime.strptime(message.text, "%d.%m.%Y")
    except ValueError:
        await message.answer(_(ct.c_input_birthday_incorrect))
        return

    user_info = await state.get_data()
    first_name = user_info.get("first_name")
    last_name = user_info.get("last_name")
    phone = user_info.get("phone")

    #  Result is recorded (updated) in the database, sent a message is user
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


@dp.message_handler(state=UserChatRegister.birthday)
async def not_valid_birth_date(message: Message):
    """ If the date format is incorrect """
    await message.answer(
        text=_(ct.c_input_birthday_again))


@dp.message_handler(
    lambda message: not message.contact, state=UserChatRegister.phone)
async def check_contact(message: Message):
    """ If a message is sent without a contact """
    await message.reply(
        text=_(ct.c_share_phone_number_not_valid),
        reply_markup=get_contact_keyboard()
    )


@dp.message_handler(state=UserChatRegister.yes_or_no)
async def not_pressed_yes_or_cancel(message: Message):
    """ If the yes or cancel button was not pressed """
    await message.answer(
        text=_(ct.c_take_approval),
        reply_markup=make_buttons(words=[ct.c_yes, ct.c_cancel], row_width=2)
    )
