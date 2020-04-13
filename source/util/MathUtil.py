def constrain(x, low, high):
    """
    限制一个数字于最低值与最高值之间

    :param x: 数字
    :param low: 最低值
    :param high: 最高值
    :return:
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
    :return:
    """
    newVal = (n - start1) / (stop1 - start1) * (stop2 - start2) + start2
    if not withinBounds:
        return newVal
    if start2 < stop2:
        return constrain(newVal, start2, stop2)
    else:
        return constrain(newVal, stop2, start2)
