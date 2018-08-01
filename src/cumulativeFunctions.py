import numpy as np


def exponentialF(x, b):
    if b < 0:
        raise Exception('Parameter b cannot be < 0')
    if x >= 0:
        return 1 - np.exp(-x / b)
    return 0


def paretoF(x, a, m):
    if a < 0:
        raise Exception('Parameter a cannot be < 0')
    if x >= m:
        return 1 - (m / x)**a
    return 0


def powerF(x, a):
    if a < 0:
        raise Exception('Parameter a cannot be < 0')
    if x >= 0 and x <= 1:
        return x**a
    return 0
