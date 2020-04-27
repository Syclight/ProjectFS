import pygame
import configparser


# 空的surface
from source.core.math.Vector import point2


def blankSurface(size, color):
    temp = pygame.Surface(size).convert()
    temp.fill(color)
    if len(color) > 3:
        temp.set_alpha(color[3])
    return temp


# 文字surface
def textSurface(text, font, size, color):
    textTemp = pygame.font.SysFont(font, size)
    return textTemp.render(text, 1, color)


# 带有文字的surface这里的
def blankTextSurface(size_WH, background_color, text, font, font_size, font_color, offset_XY):
    temp = blankSurface(size_WH, background_color)
    temp.blit(textSurface(text, font, font_size, font_color), offset_XY)
    return temp


# 裁剪资源图
def clipResImg(tarImg, rect, colorKey):
    temp = pygame.Surface((rect[2], rect[3])).convert()
    temp.set_colorkey(colorKey)
    temp.blit(tarImg, (-rect[1], -rect[0]))
    return temp


# 改变alpha值
def blitAlpha(tar, source, loc, opacity):
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)
    tar.blit(temp, loc)


# 返回水平居中的水平位置
def centeredXPos(bg_width, obj_width, bg_left=0):
    return (bg_width / 2 - obj_width / 2) + bg_left


# 返回铅直居中的水平位置
def centeredYPos(bg_height, obj_height, bg_top=0):
    return (bg_height / 2 - obj_height / 2) + bg_top


# 返回垂直位置(X, Y)
def centeredXYPos(bg_width, obj_width, bg_height, obj_height) -> []:
    return centeredXPos(bg_width, obj_width), centeredYPos(bg_height, obj_height)


# 判断pos是否在矩形区域内
def InRect(pos, rect) -> bool:
    if rect[0] + rect[2] > pos[0] > rect[0] and rect[1] < pos[1] < rect[1] + rect[3]:
        return True
    return False


# 判断pos是否在圆形区域内
def InCircular(pos, cir) -> bool:
    if pow(pow(pos[0] - cir.left, 2) + pow(pos[1] - cir.top, 2), 0.5) > cir.r:
        return False
    return True


# 判断pos是否在Element内
def InElement(pos, element) -> bool:
    if not element:
        return False
    area = element.area
    return area.contains(point2(pos))


# 判断pos是否在Sprite内
def InSprite(pos, sprite, _type=0) -> bool:
    if not sprite:
        return False
    if _type == 0:
        return InRect(pos, sprite.rect)
    elif _type == 1:
        return InCircular(pos, sprite.area)


# 读取InI文件内容
# 参数：
# @path ini文件的地址
# @section ini文件中的节点
# @param ini文件中该节点下的元素，默认为None，如果取列表的话可以不填
# 返回值：列表
# 【0】该ini文件section下，param对应的值
# 【1】ini文件section下，所有的键值对，为字典
# 【2】ini文件section下，所以得变量值
def readINI(path, section, param=None) -> list:
    conf = configparser.ConfigParser()
    conf.read(path)
    return [conf.get(section, param), conf.items(section), conf.options(section)]


# 添加INI文件中的项
def addINI(path, section, param, val):
    conf = configparser.ConfigParser()
    conf.read(path)
    if not conf.has_section(section):
        conf.add_section(section)
    conf.set(section, param, val)
    conf.write(open(path, "w+"))


# 修改INI文件
def updateINI(path, section, param, val):
    conf = configparser.ConfigParser()
    conf.read(path)
    conf.set(section, param, val)
    conf.write(open(path, "w+"))


# 读取INI文件内容为int
def readINIInt(path, section, param):
    return int(readINI(path, section, param)[0])


# 读取INI文件内容为bool
def readINIBool(path, section, param):
    return bool(readINIInt(path, section, param))


# 读取INI文件内容为Float
def readINIFloat(path, section, param):
    return float(readINI(path, section, param)[0])


# 将数字转换成中文字符串
# @param int num 要转换的数字 eg. 123, 567
# @param Const.NUM_DICT mapping 对应规则， 在Const.py 中定义的NUM_DICT系列常量
# @ret str 对应规则下的字符串
def IntToStr(num, mapping) -> str:
    s = str(num)
    res = ''
    for c in s:
        res += mapping[c]
    return res


# 将中文字符串转换成数字
# @param str s 要转换的字符串，必须在 Const.NUM_DICT 中有对应关系
# @param Const.NUM_DICT mapping 对应规则， 在Const.py 中定义的NUM_DICT系列常量
# @ret int 对应规则下的数字
def StrToInt(s, mapping) -> int:
    new_dict = {v: k for k, v in mapping.items()}
    res = ''
    for c in s:
        res += new_dict[c]
    return int(res)


# 归并排序:
def MergeSort(lists) -> list:
    if len(lists) <= 1:
        return lists
    num = int(len(lists) / 2)
    left = MergeSort(lists[:num])
    right = MergeSort(lists[num:])
    return Merge(left, right)


def Merge(left, right):
    rt, lf = 0, 0
    result = []
    while lf < len(left) and rt < len(right):
        if left[lf] <= right[rt]:
            result.append(left[lf])
            lf += 1
        else:
            result.append(right[rt])
            rt += 1
    result += list(left[lf:])
    result += list(right[rt:])
    return result


# 针对Ioevent3Enum的转换器,将pygameKey转换成IoEvent3的Key
def exKey(key) -> int:
    return int(key) - 97 + 0xC0000


# 将Shape.py中的形状转换为pygame.Rect
def ex_toRect(rect) -> pygame.Rect:
    return pygame.Rect(rect.x, rect.y, rect.w, rect.h)


# 在一维容器中选出非n数的地址值
def getNotN(container, n) -> list:
    res = []
    i = 0
    for b in container:
        if b != n:
            res.append(i)
        i += 1
    return res
