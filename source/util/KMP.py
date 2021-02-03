def get_next_group(one_str) -> list:
    """ 获取到next数组 """
    length = len(one_str)
    next_group = [0] * length
    next_group[0] = -1
    point = -1
    i = 0
    while i < length - 1:
        if point == -1 or one_str[i] == one_str[point]:
            point += 1
            i += 1
            next_group[i] = point
        else:
            point = next_group[point]
    return next_group


def KMPMatching(s, t) -> int:
    """
    KMP算法匹配字符串
    :param s:要匹配的字符串
    :param t:模式串
    :return:int 要匹配的字符串中的索引, 匹配失败返回-1
    """
    nextGroup = get_next_group(t)
    j, i = -1, -1
    while j != len(t) and i < len(s):
        if s[i] == t[j] or j == -1:
            i, j = i + 1, j + 1
        else:
            j = nextGroup[j]
    return i - j if j == len(t) else -1


print(KMPMatching('ababxbabcdabdfdsss', 'aba'))
