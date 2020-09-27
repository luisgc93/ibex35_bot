from apscheduler.schedulers.blocking import BlockingScheduler
from . import bot

sched = BlockingScheduler()


@sched.scheduled_job("cron", day_of_week="mon-sat", hour=10)
def scheduled_job():
    bot.scrape_el_economista()


sched.start()
