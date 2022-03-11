import time

import pytest
from distribute_challenge import FunctionFailedError, compute_this


@compute_this()
def my_func(x):
    time.sleep(x)
    return x * x


@compute_this()
def error_func(x):
    raise Exception('bad function')


def test_compute_this():
    out = my_func(2).run()
    assert out == 4


def test_compute_this_when_func_raises_exception():
    with pytest.raises(FunctionFailedError):
        error_func(2).run()
