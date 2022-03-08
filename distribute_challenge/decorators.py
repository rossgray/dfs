import functools
from distribute_challenge.service import DistributedFunctionService

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


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
            ready = kwargs.pop('__ready', False)
            if ready is True:
                return func(*args, **kwargs)
            else:
                logger.info('Inside wrapper_compute_this')
                distributed = DistributedFunctionService(func, *args, **kwargs)
                return distributed

        return wrapper_compute_this

    return decorator_compute_this
