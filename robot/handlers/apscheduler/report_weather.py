from datetime import datetime, timedelta

from loader import scheduler
from robot.handlers.users.misc import cmd_weather


#  Once a day
scheduler.add_job(
    cmd_weather,
    name="BD",
    trigger="cron",
    hour=19,
    minute=51,
)
