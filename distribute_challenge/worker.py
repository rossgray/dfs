from rq import Worker, Connection
from distribute_challenge.service import queue, redis_conn

import logging

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

with Connection(redis_conn):
    worker = Worker([queue])
    worker.work()
