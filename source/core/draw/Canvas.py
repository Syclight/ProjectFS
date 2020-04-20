import pygame

from source.core.draw.Color import color
from source.core.math.Vector import vec2


class canvas:
    """画布，可进行alpha混合"""

    def __init__(self, *args):
        col, e = args[0], args[1]

        self.__suf = None
        self.__recordPix = []
        self.width, self.height = 0, 0

        if isinstance(e, vec2):
            self.width, self.height = int(e.x), int(e.y)
            self.__suf = pygame.Surface((self.width, self.height)).convert()
        elif isinstance(e, pygame.Surface):
            self.width, self.height = e.get_width(), e.get_height()
            self.__suf = e.copy()

        self.__init(col)

    def __init(self, col):
        self.__recordPix = [col] * self.width * self.height
        self.__suf.fill(col.aryRGBA())

    def setSurface(self, suf):
        self.__suf = suf.copy()

    def surface(self):
        return self.__suf

    def getPix(self, x, y):
        return self.__recordPix[y * self.width + x]

    def setPix(self, x, y, col):
        _col = self.getPix(x, y)
        _col = color.mix_(col, _col)
        self.__recordPix[y * self.width + x] = _col
        self.__suf.set_at([x, y], _col.aryRGB())

    def fill(self, col):
        self.__init(col)
