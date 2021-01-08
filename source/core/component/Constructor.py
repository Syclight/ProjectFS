from source.core.const.Const import gl_Font
from source.core.math.Vector import vec2
from source.util.ToolsFuc import centeredXPos, centeredYPos, centeredXYPos
from source.view.element.Elements import TextElement


class Constructor:
    """Element 生成器，可以生成Element"""
    nextElementY = 0
    id = 0

    TOP, LEFT, RIGHT, BOTTOM = 0, 1, 2, 3
    TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT = 10, 11, 12, 13
    CENTER = 99

    __CreatedElementList = list()

    def __init__(self, render, rect):
        self.__render = render
        self.__rect = rect

    def __getPos(self, x, length, size):
        if x == 0:
            return centeredXPos(self.__rect.w, length), 0
        if x == 1:
            return 0, centeredYPos(self.__rect.h, length)
        if x == 2:
            return self.__rect.w - length, centeredYPos(self.__rect.h, length)
        if x == 3:
            return centeredXPos(self.__rect.w, length), self.__rect.h - size
        if x == 10:
            return 0, 0
        if x == 11:
            return self.__rect.w - length, 0
        if x == 12:
            return 0, self.__rect.h - size
        if x == 13:
            return self.__rect.w - length, self.__rect.h - size
        if x == 99:
            return centeredXYPos(self.__rect.w, length, self.__rect.h, size)

    def getCreatedElement(self, index):
        return self.__CreatedElementList[index]

    def createTextElement(self, text="TextElement", pos=(0, 0), size=18, length=None, color=(255, 255, 255),
                          font=gl_Font, zIndex=999):
        """

        :param text:
        :param pos: 可以是int型数字代码， 0，上居中
        :param size:
        :param length:
        :param color:
        :param font:
        :param zIndex:
        :return:
        """
        if length is None:
            length = len(text) * size
        _top, _left = 0, self.nextElementY
        if isinstance(pos, tuple) or isinstance(pos, list):
            _top, _left = pos[0], self.nextElementY + pos[1]
        elif isinstance(pos, vec2):
            _top, _left = pos.x, self.nextElementY + pos.y
        elif isinstance(pos, int):
            _top, _left = self.__getPos(pos, length, size)

        e = TextElement((_top, _left, length * size + 2, size + 2), text, font, size, color, 1)
        e.zIndex = zIndex
        self.__CreatedElementList.append(e)
        self.__render.open()
        self.__render.add(e)
        self.__render.close()
        self.nextElementY += size + 4
        self.id += 1
        return e
