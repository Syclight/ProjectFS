import pygame

from source.core.draw.Color import color
from source.core.exception.SGFpyException import SGFpyException
from source.core.math.MathUtil import mapping
from source.core.math.Vector import vec3


class outOfRangeException(SGFpyException):
    def __init__(self, num, limit):
        self.num = num
        self.limit = limit

    def __str__(self):
        return '{} out of limit RectRange{}'.format(self.num, self.limit)


class brush:
    def __init__(self, canvas, _color, width):
        self.width = width
        a = _color[3] if len(_color) > 3 else 1
        self.color = color(_color[0], _color[1], _color[2], a)
        self.canvas = canvas

    def drawLine(self, start, stop, aa=0):
        # pix = []
        x1, y1, x2, y2 = int(start[0]), int(start[1]), int(stop[0]), int(stop[1])
        if x1 > self.canvas.width or x1 < 0 or y1 > self.canvas.height or y1 < 0 \
                or x2 > self.canvas.width or x2 < 0 or y2 > self.canvas.height or y2 < 0:
            raise outOfRangeException(((x1, y1), (x2, y2)), (0, 0, self.canvas.width, self.canvas.height))
        dx, dy, yy = int(abs(x2 - x1)), int(abs(y2 - y1)), 0

        if dx < dy:
            yy = 1
            x1, y1 = y1, x1
            x2, y2 = y2, x2
            dx, dy = dy, dx

        ix = 1 if x2 - x1 > 0 else -1
        iy = 1 if y2 - y1 > 0 else -1
        cx, cy = x1, y1
        n2dy, n2dydx = dy * 2, (dy - dx) * 2
        d = dy * 2 - dx

        if yy:  # 直线与x轴大于45度
            while cx != x2:
                if d < 0:
                    d += n2dy
                else:
                    cy += iy
                    d += n2dydx
                # pix.append((cy, cx))
                self.canvas.setPix(cy, cx, self.color)
                cx += ix
        else:  # 直线与x轴小于等于45度
            while cx != x2:
                if d < 0:
                    d += n2dy
                else:
                    cy += iy
                    d += n2dydx
                # pix.append((cx, cy))
                self.canvas.setPix(cx, cy, self.color)

                cx += ix

        # if aa:
        #     pygame.draw.aaline(self.canvas.surface(), self.color.aryRGB(), start, stop, 1)
        # else:
        #     pygame.draw.line(self.canvas.surface(), self.color.aryRGB(), start, stop, self.width)
