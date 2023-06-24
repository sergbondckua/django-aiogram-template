from datetime import datetime

from aiogram.types import Message
from aiogram.utils.markdown import quote_html

from loader import _
from robot.models import DeepLink


async def get_deeplink(link: str, tg_object: Message):
    month_year = datetime.now().strftime("%B-%Y")
    userid = tg_object.from_user.id
    full_name = tg_object.from_user.full_name

    try:
        query = await DeepLink.objects.aget(link=link)
    except DeepLink.DoesNotExist:
        await tg_object.answer(
            text=_("Інформації не знайдено"),
        )
        return
    await tg_object.answer(
            text=query.message.format(
                userid=userid,
                month_year=month_year,
                full_name=quote_html(full_name.replace(" ", "_")),
            ),
        )
