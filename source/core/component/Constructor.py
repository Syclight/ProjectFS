from source.core.math.Vector import vec2
from source.util.ToolsFuc import centeredXPos
from source.view.element.Elements import TextElement, gl_Font


class Constructor:
    nextElementY = 0
    id = 0

    TOP, LEFT, RIGHT, BOTTOM = 0, 1, 2, 3
    TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT = 10, 11, 12, 13
    CENTER = 99

    def __init__(self, render, rect):
        self.__render = render
        self.__rect = rect

    def createTextElement(self, text, pos=(0, 0), size=18, color=(255, 255, 255)):
        length = len(text)
        _top, _left = 0, self.nextElementY
        if isinstance(pos, tuple) or isinstance(pos, list):
            _top, _left = pos[0], self.nextElementY + pos[1]
        elif isinstance(pos, vec2):
            _top, _left = pos.x, self.nextElementY + pos.y

        e = TextElement((_top, _left, length * size + 2, size + 2), text, gl_Font, size, color, 1)
        self.__render.open()
        self.__render.add(e)
        self.__render.close()
        self.nextElementY += size + 4
        self.id += 1
        return e
