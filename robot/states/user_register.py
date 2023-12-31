from aiogram.dispatcher.filters.state import StatesGroup, State


class UserRegister(StatesGroup):
    username = State()
    first_name = State()
    last_name = State()
    password = State()


class UserChatRegister(StatesGroup):
    yes_or_no = State()
    phone = State()
    first_name = State()
    last_name = State()
    birthday = State()
