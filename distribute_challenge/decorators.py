import functools

from distribute_challenge.service import DistributedFunctionService


def compute_this():
    """
    Decorator to mark a function for submission to distributed function
    service.

    Note, this is a wrapper over a decorator since compute_this can be called
    with arguments. If decorator were to be used purely as:

    @compute_this
    def func(x):
        ...

    then this could be simplified.
    """

    def decorator_compute_this(func):
        @functools.wraps(func)
        def wrapper_compute_this(*args, **kwargs):
            # The rq library queues functions based on their import path. This
            # does not play nicely with our decorated functions, since it tries
            # to put the decorated function on the queue rather than the inner
            # function. Therefore, we add a special '__ready' kwarg inside the
            # DistributedFunctionService and then when this decorator is called
            # by an rq worker we know to execute the inner function rather than
            # queuing it again.
            ready = kwargs.pop('__ready', False)
            if ready is True:
                return func(*args, **kwargs)
            else:
                # if __ready kwarg not set, we return an instance of
                # DistributedFunctionService so that it can be queued later
                # when run() is called
                distributed = DistributedFunctionService(func, *args, **kwargs)
                return distributed

        return wrapper_compute_this

    return decorator_compute_this
