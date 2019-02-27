import numpy as np


def exponential_cumulative(x, b):
    """
    """
    if b < 0:
        raise Exception('Parameter b cannot be < 0')
    if x >= 0:
        return 1 - np.exp(-x / b)
    return 0


def pareto_cumulative(x, a, m):
    if a < 0:
        raise Exception('Parameter a cannot be < 0')
    if x >= m:
        return 1 - (m / x)**a
    return 0


def power_cumulative(x, a):
    """Returns the probability [0,1) of being in an active state
    following a power law P(x;a) ~ x ^ - (a + 1)
    """
    xmin = 2
    if a <= 0:
        raise Exception('Parameter a cannot be < 0')
    if x >= 1:
        return (x / xmin)**(-a + 1)
    return -1


def pwlaw(min=1, max=30, exponent=2., size=1):
    """Power-law gen for pdf(x)\propto x^{exponent-1} for min<=x<=max"""
    r = np.random.random(size=size)
    ag, bg = min**exponent, max**exponent
    return (ag + (bg - ag) * r)**(1. / exponent)
