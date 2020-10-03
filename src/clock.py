import random

from apscheduler.schedulers.blocking import BlockingScheduler
from . import bot

sched = BlockingScheduler()


@sched.scheduled_job("cron", day_of_week="mon-sat", hour=10)
def scheduled_job():
    random.choice([bot.scrape_el_economista(), bot.scrape_bolsamania()])


sched.start()
