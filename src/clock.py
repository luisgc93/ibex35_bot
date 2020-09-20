from . import bot
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=2)
def timed_job():
    bot.scrape_el_economista()


@sched.scheduled_job('cron', day_of_week='mon-sat', hour=10)
def scheduled_job():
    bot.scrape_el_economista()


sched.start()
