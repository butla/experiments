import random
import time

from huey.contrib.sql_huey import SqlHuey
import peewee


database = peewee.PostgresqlDatabase(
    database='postgres',
    user='postgres',
    password='postgres',
    host='localhost',
    port=5432,
)
# TODO initialize that later, not during import
huey = SqlHuey(database=database)


@huey.task()
def delayed_random(delay: int):
    time.sleep(delay)
    print('finishing up the task')
    return random.random()
