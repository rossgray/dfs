import os

from fakeredis import FakeStrictRedis
from redis import Redis
from rq import Queue

ENV = os.getenv("ENV")
REDIS_HOST = os.getenv("REDIS_HOST")


def get_redis_conn():
    if ENV == 'test':
        return FakeStrictRedis()
    else:
        return Redis(host=REDIS_HOST)


def get_queue(redis_conn):
    is_async = True
    if ENV == 'test':
        is_async = False

    return Queue(is_async=is_async, connection=redis_conn)
