from os import environ

from peewee import BigIntegerField, Model
from playhouse.db_url import connect

db = connect(environ["DATABASE_URL"])


class Mention(Model):
    tweet_id = BigIntegerField()

    class Meta:
        database = db
        table_name = "mentions"
