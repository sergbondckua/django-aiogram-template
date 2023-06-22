from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from const_texts import c_share_phone_number, c_cancel
from loader import _


def make_buttons(words: list, row_width: int = 1) -> ReplyKeyboardMarkup:
    buttons_group = ReplyKeyboardMarkup(
        row_width=row_width,
        resize_keyboard=True,
    )
    for word in words:
        if word is not None:
            buttons_group.insert(KeyboardButton(text=_(word)))
    return buttons_group


def get_contact_keyboard() -> ReplyKeyboardMarkup:
    contact_request_button = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text=_(c_share_phone_number), request_contact=True)],
            [KeyboardButton(text=_(c_cancel))],
        ],
    )
    return contact_request_button
