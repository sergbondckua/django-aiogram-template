from aiogram.utils.deep_linking import get_start_link
from aiogram import types

from loader import dp


# хендлер для создания ссылок
@dp.message_handler(commands=["ref"])
async def get_ref(message: types.Message):
    link = await get_start_link(str(message.from_user.username), encode=True)
    # result: 'https://t.me/MyBot?start='
    #  после знака = будет закодированный никнейм юзера, который создал реф ссылку, вместо него можно вставить и его id
    await message.answer(f"Ваша реф. ссылка {link}")
