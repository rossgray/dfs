import time

from distribute_challenge import compute_this


@compute_this()
def my_func(x):
    time.sleep(x)
    return x * x


def test_compute_this():
    out = my_func(2).run()
    assert out == 4
