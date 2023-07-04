from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from django.conf import settings

from robot.middlewares import ThrottlingMiddleware
from robot.middlewares.language import setup_middleware

bot = Bot(token=settings.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
scheduler = AsyncIOScheduler(timezone=settings.TIME_ZONE)

# Set up i18n middleware to work with multilingualism
i18n = setup_middleware(dp)

# Alias for gettext method
_ = i18n.gettext


# Set up throttling middleware
dp.middleware.setup(ThrottlingMiddleware())
