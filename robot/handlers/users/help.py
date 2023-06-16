from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from aiogram.utils.deep_linking import get_start_link

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Команди: ", "/start - Запустіть бота", "/help - Довідка")

    await message.answer("\n".join(text))


# хендлер для создания ссылок
@dp.message_handler(commands=["ref"])
async def get_ref(message: types.Message):
    link = await get_start_link("urlpay", encode=True)
    # result: 'https://t.me/MyBot?start='
    #  после знака = будет закодированный никнейм юзера, который создал реф ссылку, вместо него можно вставить и его id
    await message.answer(f"Ваша реф. ссылка {link}")
