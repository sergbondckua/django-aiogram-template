from loader import bot, dp
from robot.models import TelegramUser


async def get_user_avatar(userid: str) -> str | None:
    """Returns the avatar id for a user"""
    photos = await bot.get_user_profile_photos(
        user_id=userid, offset=-1, limit=1)
    if not photos.total_count:
        return None

    avatar = photos.photos[0][0]
    avatar_id = avatar.file_id
    return avatar_id


async def send_message_to_bot_admins(msg: str) -> None:
    """Sends a message to the bot all admins"""
    async for admin in TelegramUser.objects.filter(is_admin=True):
        await dp.bot.send_message(admin.userid, msg)
