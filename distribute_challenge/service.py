import time
import os
from redis import Redis
from rq import Queue

ENV = os.getenv("ENV")
REDIS_HOST = os.getenv("REDIS_HOST")

queue = None
redis_conn = None
if ENV == 'test':
    from fakeredis import FakeStrictRedis

    queue = Queue(is_async=False, connection=FakeStrictRedis())
else:
    redis_conn = Redis(host=REDIS_HOST)
    queue = Queue(connection=redis_conn)


class DistributedFunctionService:
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        kwargs = self.kwargs
        kwargs['__ready'] = True
        job = queue.enqueue(self.func, args=self.args, kwargs=kwargs)
        # TODO - add error handling
        while job.result is None:
            time.sleep(0.1)
        return job.result
