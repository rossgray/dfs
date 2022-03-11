"""Starts an rq worker"""
from rq import Connection, Worker

from distribute_challenge.service import queue, redis_conn

with Connection(redis_conn):
    worker = Worker([queue])
    worker.work()
