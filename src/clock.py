import os
from apscheduler.schedulers.blocking import BlockingScheduler

import os
for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        print(os.path.join(root, name))
    for name in dirs:
        print(os.path.join(root, name))

from src import bot

sched = BlockingScheduler()


@sched.scheduled_job("interval", minutes=2)
def timed_job():
    bot.scrape_el_economista()


@sched.scheduled_job("cron", day_of_week="mon-sat", hour=10)
def scheduled_job():
    bot.scrape_el_economista()


sched.start()
