import random

from apscheduler.schedulers.blocking import BlockingScheduler

from . import bot, const

sched = BlockingScheduler()


@sched.scheduled_job("cron", day_of_week="mon-sat", hour=10)
def scheduled_job():
    site = random.choice(const.SITES)
    home_url = site.get("home_url")
    xpath = site.get("xpath")
    bot.scrape_website(home_url, xpath)


sched.start()
