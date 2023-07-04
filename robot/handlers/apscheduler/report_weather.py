from datetime import datetime, timedelta

from loader import scheduler
from robot.handlers.users.misc import cmd_weather

#  Once a day
scheduler.add_job(
    cmd_weather,
    trigger="cron",
    hour=00,
    minute=21,
)
