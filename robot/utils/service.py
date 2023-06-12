from loader import bot


async def get_user_avatar(userid: str) -> str | None:
    """Returns the avatar id for a user"""
    photos = await bot.get_user_profile_photos(
        user_id=userid, offset=-1, limit=1)
    if not photos.total_count:
        return None

    avatar = photos.photos[0][0]
    avatar_id = avatar.file_id
    return avatar_id
