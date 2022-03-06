import functools


def compute_this():
    """
    This is a wrapper over a decorator since compute_this can be called with
    arguments. If decorator were to be used purely as:

    @compute_this
    def func(x):
        ...

    then this could be simplified.
    """

    def decorator_compute_this(func):
        @functools.wraps(func)
        def wrapper_compute_this(*args, **kwargs):
            distributed = DistributedFunctionService(func, *args, **kwargs)
            return distributed

        return wrapper_compute_this

    return decorator_compute_this


class DistributedFunctionService:
    def __init__(self, func, *args, **kwargs):
        self._func = func
        self._args = args
        self._kwargs = kwargs

    def run(self):
        return self._func(*self._args, **self._kwargs)
