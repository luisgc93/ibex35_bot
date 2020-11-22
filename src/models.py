from os import environ

from peewee import BigIntegerField, Model
from playhouse.db_url import connect

db = connect(environ["DATABASE_URL"])


class BaseModel(Model):
    class Meta:
        database = db


class Mention(BaseModel):
    tweet_id = BigIntegerField()

    class Meta:
        table_name = "mentions"
