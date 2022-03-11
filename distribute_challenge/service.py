import time

from distribute_challenge.config import get_queue, get_redis_conn

redis_conn = get_redis_conn()
queue = get_queue(redis_conn)


class FunctionFailedError(Exception):
    """Raised when a function fails during execution"""


class DistributedFunctionService:
    """A service for running functions using a distributed worker
    architecture.
    """

    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        """Places the function in an rq queue where it will be consumed by one
        of the workers. Since this function needs to return a result
        synchronously to the client, we wait until the job has been executed
        and then return the result.

        We add a special '__ready' kwarg to the function to enqueue as
        as a workaround due to a limitation in the way the rq library works:

        The rq library queues functions based on their import path. This
        does not play nicely with our decorated functions, since the function
        being queued is not the inner function but our decorated function,
        meaning we end up stuck in a loop.

        When the worker comes to execute our function it sees this argument and
        knows to execute the inner function directly rather than enqueuing it
        again. (See compute_this decorator in decorators.py for reference)
        """
        kwargs = self.kwargs
        kwargs['__ready'] = True
        job = queue.enqueue(self.func, args=self.args, kwargs=kwargs)
        while job.result is None:
            # if job failed, raise an exception
            if job.is_failed is True:
                raise FunctionFailedError
            time.sleep(0.1)
        return job.result
