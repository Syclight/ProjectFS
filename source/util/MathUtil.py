from math import cos, pi

__all__ = [
    'constrain', 'mapping',
    'interpolation_lin', 'interpolation_cos', 'interpolation_cubic', 'interpolation_hermite', 'interpolation_hermite'
]


def constrain(x, low, high):
    """
    限制一个数字于最低值与最高值之间

    :param x: 数字
    :param low: 最低值
    :param high: 最高值
    :return: number
    """
    return max(min(x, high), low)


def mapping(n, start1, stop1, start2, stop2, withinBounds=True):
    """
    从一个范围内映射一个数字去另一个范围

    :param n: 要映射的数字
    :param start1: 范围1开始
    :param stop1: 范围1结束
    :param start2: 范围2开始
    :param stop2: 范围2结束
    :param withinBounds: 是否限制在新范围的最高值和最低值之间
    :return: number
    """
    newVal = (n - start1) / (stop1 - start1) * (stop2 - start2) + start2
    if not withinBounds:
        return newVal
    if start2 < stop2:
        return constrain(newVal, start2, stop2)
    else:
        return constrain(newVal, stop2, start2)


def interpolation_lin(a, b, amt):
    return amt * (b - a) + a


def interpolation_cos(a, b, amt):
    _amt = (1 - cos(amt * pi)) / 2
    return _amt * (b - a) + a


def interpolation_cubic(a, b, c, d, amt):
    """ b: great than a less then c

    c: less than d great than b"""
    _amt = amt * amt
    _a = d - c - a + b
    _b = a - b - _a
    _c = c - a
    _d = b
    return _a * _amt * amt + _b * _amt + _c * amt + _d


def interpolation_hermite(a, b, c, d, amt, tension, bias):
    """tension: 1 is high, 0 is normal, -1 is

    low,bias: 0 is even, positive is towards first segment, negative towards the other"""
    _amt0 = amt * amt
    _amt1 = _amt0 * amt

    m0 = (b - a) * (1 + bias) * (1 - tension) / 2
    m0 += (c - b) * (1 - bias) * (1 - tension) / 2
    m1 = (c - b) * (1 + bias) * (1 - tension) / 2
    m1 += (d - c) * (1 - bias) * (1 - tension) / 2

    _a = 2 * _amt1 - 3 * _amt0 + 1
    _b = _amt1 - 2 * _amt0 + amt
    _c = _amt1 - _amt0
    _d = -2 * _amt1 + 3 * _amt0

    return _a * b + _b * m0 + _c * m1 + _d * c
