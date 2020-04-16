import pygame

__all__ = [
    'Painter',
]


class Painter:
    """将pygame.draw包装，可直接绘制Shape类型的图形,方便框架使用

    因为使用pygame.draw，在线框模式下如果开启抗锯齿则width参数的值固定为1

    绘制圆和椭圆时，抗锯齿无效"""

    def __init__(self, surf):
        self.s = surf

    def Pixel(self, p, color):
        """
        绘制一个像素点

        :param p: Math2d::vec2 or Math2d::point2
        :param color: tuple (R, G, B)
        :return: None
        """
        self.s.set_at([int(p.x), int(p.y)], color)

    def Line(self, line, color, width, aa=0):
        """
        绘制直线

        :param line: Shape::Line
        :param color: tuple (R, G, B)
        :param width: int 线宽
        :param aa: bool 是否抗锯齿
        :return: None
        """
        sp = (int(line.pos.x), int(line.pos.y))
        eps = line.dir.setLen(line.length)
        ep = (sp[0] + int(eps.x), sp[1] + int(eps.y))
        if aa:
            pygame.draw.aaline(self.s, color, sp, ep, 1)
        else:
            pygame.draw.line(self.s, color, sp, ep, width)

    def Lines(self, points, color, width, closed, aa=0):
        """
        绘制连续的直线

        :param points: list len >= 2 if len < 2 ret
        :param color: tuple (R, G, B)
        :param width: int 线宽
        :param closed: bool 是否闭合
        :param aa: bool 是否抗锯齿
        :return: None
        """
        length = len(points)
        if length < 2:
            return

        for i in range(0, length - 1):
            p0, p1 = points[i], points[i + 1]
            _p0, _p1 = (int(p0.x), int(p0.y)), (int(p1.x), int(p1.y))
            if aa:
                pygame.draw.aaline(self.s, color, _p0, _p1, 1)
            else:
                pygame.draw.line(self.s, color, _p0, _p1, width)
        if closed:
            sp, ep = points[0], points[length - 1]
            _sp, _ep = (int(sp.x), int(sp.y)), (int(ep.x), int(ep.y))
            if aa:
                pygame.draw.aaline(self.s, color, _ep, _sp, 1)
            else:
                pygame.draw.line(self.s, color, _ep, _sp, width)

    def Arc(self, color, rect, start_angle, stop_angle, width):
        """
        绘制一条曲线

        :param color: tuple (R, G, B)
        :param rect: Shape::Rectangle 指定弧线所在的椭圆外围的限定矩形
        :param start_angle: angle 指定弧线的开始位置
        :param stop_angle: angle 指定弧线的结束位置
        :param width: int 线宽
        :return: None
        """
        _rect = (rect.x, rect.y, rect.w, rect.h)
        pygame.draw.arc(self.s, color, _rect, start_angle, stop_angle, width)

    def Rect(self, rect, color, width, aa=0):
        """
        绘制矩形

        :param rect: Shape::Rectangle
        :param color: tuple (R, G, B)
        :param width: int 线宽 0表示填充
        :param aa: bool 是否抗锯齿
        :return: None
        """
        _rect = (rect.x, rect.y, rect.w, rect.h)
        if width == 0:
            pygame.draw.rect(self.s, color, _rect, 0)
            if aa:
                points = rect.array()
                self.Lines(points, color, 1, 1, 1)
        else:
            points = rect.array()
            self.Lines(points, color, width, 1, aa)

    def Triangle(self, triangle, color, width, aa):
        """
        绘制一个三角形

        :param triangle: Shape::Triangle
        :param color: tuple (R, G, B)
        :param width: int 线宽 0表示填充
        :param aa: bool 是否抗锯齿
        :return: None
        """
        points = [triangle.p1, triangle.p2, triangle.p3]
        self.Polygon(points, color, width, aa)

    def Polygon(self, points, color, width, aa=0):
        """
        绘制一个多边形

        :param points: list [Math2d::vec2] or [Math2d::point2], and len >= 3 else ret
        :param color: tuple (R, G, B)
        :param width: int 线宽 0表示填充
        :param aa: bool 是否抗锯齿
        :return: None
        """
        if len(points) < 3:
            return
        if width == 0:
            _points = []
            for p in points:
                _points.append((int(p.x), int(p.y)))
            pygame.draw.polygon(self.s, color, _points, width)
            if aa:
                self.Lines(points, color, 1, 1, 1)
        else:
            self.Lines(points, color, width, 1, aa)

    def Circle(self, circle, color, width, aa=0):
        """
        绘制一个圆

        :param circle: Shape::Circle
        :param color: tuple (R, G, B)
        :param width: int 线宽 0表示填充
        :param aa: bool 是否抗锯齿
        :return: None
        """
        pos = (int(circle.x), int(circle.y))
        radius = int(circle.r)
        pygame.draw.circle(self.s, color, pos, radius, width)

    def Ellipse(self, ellipse, color, width, aa=0):
        """
        绘制一个椭圆

        :param ellipse: Shape::Ellipse
        :param color: tuple (R, G, B)
        :param width: int 线宽 0表示填充
        :param aa: bool 是否抗锯齿
        :return: None
        """
        rect = (ellipse.x - ellipse.a, ellipse.y - ellipse.b, ellipse.a * 2, ellipse.b * 2)
        pygame.draw.ellipse(self.s, color, rect, width)
