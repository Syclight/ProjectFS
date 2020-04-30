import pygame

__all__ = [
    'Painter',
]

from source.core.component.Transform import Transform
from source.core.math.Vector import vec3


class Painter(Transform):
    """将pygame.draw包装，可直接绘制Shape类型的图形,方便框架使用

    因为使用pygame.draw，在线框模式下如果开启抗锯齿则width参数的值固定为1

    绘制圆和椭圆时，抗锯齿无效"""

    def __init__(self, surf, onSurf=False):
        super().__init__()
        self.s = surf
        self.on = onSurf

    def Pixel(self, p, color):
        """
        绘制一个像素点

        :param p: Math2d::vec2 or Math2d::point2
        :param color: tuple (R, G, B)
        :return: None
        """

        v = super().getCurrentMat().mul_vec3(vec3(p.x, p.y, 1))
        self.s.set_at([int(v.x), int(v.y)], color)

    def Line(self, line, color, width, aa=0):
        """
        绘制直线

        :param line: Shape::Line
        :param color: tuple (R, G, B)
        :param width: int 线宽
        :param aa: bool 是否抗锯齿
        :return: None
        """
        v = super().getCurrentMat().mul_vec3(vec3(line.pos.x, line.pos.y, 1))
        sp = (int(v.x), int(v.y))
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
        sp, ep = None, None
        length = len(points)
        if length < 2:
            return
        for i in range(0, length - 1):
            p0, p1 = points[i], points[i + 1]
            _p0, _p1 = (int(p0[0]), int(p0[1])), (int(p1[0]), int(p1[1]))
            v0 = super().getCurrentMat().mul_vec3(vec3(_p0[0], _p0[1], 1))
            v1 = super().getCurrentMat().mul_vec3(vec3(_p1[0], _p1[1], 1))
            if i == 0:
                sp = v0
            if i == length - 2:
                ep = v1
            if aa:
                pygame.draw.aaline(self.s, color, (v0.x, v0.y), (v1.x, v1.y), 1)
            else:
                pygame.draw.line(self.s, color, (v0.x, v0.y), (v1.x, v1.y), width)
        if closed:
            if aa:
                pygame.draw.aaline(self.s, color, (sp.x, sp.y), (ep.x, ep.y), 1)
            else:
                pygame.draw.line(self.s, color, (sp.x, sp.y), (ep.x, ep.y), width)

    def Arc(self, rect, start_angle, stop_angle, color, width):
        """
        绘制一条曲线

        :param color: tuple (R, G, B)
        :param rect: Shape::Rectangle 指定弧线所在的椭圆外围的限定矩形
        :param start_angle: angle 指定弧线的开始角度
        :param stop_angle: angle 指定弧线的结束角度
        :param width: int 线宽
        :return: None
        """
        v = super().getCurrentMat().mul_vec3(vec3(rect.x, rect.y, 1))
        _rect = (v.x, v.y, rect.w, rect.h)
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
        v = super().getCurrentMat().mul_vec3(vec3(rect.x, rect.y, 1))
        _rect = (v.x, v.y, rect.w, rect.h)
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
        v1 = super().getCurrentMat().mul_vec3(vec3(triangle.p1, 1))
        v2 = super().getCurrentMat().mul_vec3(vec3(triangle.p2, 1))
        v3 = super().getCurrentMat().mul_vec3(vec3(triangle.p3, 1))
        points = [v1.ex_vec2(), v2.ex_vec2(), v3.ex_vec2()]
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

        _points = []
        for p in points:
            v = super().getCurrentMat().mul_vec3(vec3(p, 1))
            _points.append((int(v.x), int(v.y)))

        pygame.draw.polygon(self.s, color, _points, width)

        if width == 0 and aa:
            self.Lines(_points, color, 1, 1, 1)

    def Circle(self, circle, color, width, aa=0):
        """
        绘制一个圆

        :param circle: Shape::Circle
        :param color: tuple (R, G, B)
        :param width: int 线宽 0表示填充
        :param aa: bool 是否抗锯齿
        :return: None
        """
        if isinstance(circle, list) or isinstance(circle, tuple):
            pos = (int(circle[0]), int(circle[1]))
            radius = int(circle[2])
        else:
            pos = (int(circle.x), int(circle.y))
            radius = int(circle.r)
        _pos = super().getCurrentMat().mul_vec3(vec3(pos[0], pos[1], 1))
        if self.on:
            temp = pygame.Surface((radius * 2, radius * 2)).convert_alpha()
            if len(color) > 3:
                temp.set_alpha(color[3])
            pygame.draw.circle(temp, color, (radius, radius), radius, width)
            self.s.blit(temp, (_pos[0] - radius, _pos[1] - radius))
        else:
            pygame.draw.circle(self.s, color, _pos.ary(4), radius, width)

    def Ellipse(self, ellipse, color, width, aa=0):
        """
        绘制一个椭圆

        :param ellipse: Shape::Ellipse
        :param color: tuple (R, G, B)
        :param width: int 线宽 0表示填充
        :param aa: bool 是否抗锯齿
        :return: None
        """
        v = super().getCurrentMat().mul_vec3(vec3(ellipse.x, ellipse.y, 1))
        rect = (v.x - ellipse.a, v.y - ellipse.b, ellipse.a * 2, ellipse.b * 2)
        if self.on:
            temp = pygame.Surface((ellipse.a * 2, ellipse.b * 2)).convert_alpha()
            if len(color) > 3:
                temp.set_alpha(color[3])
            pygame.draw.ellipse(temp, color, temp.get_rect(), width)
            self.s.blit(temp, (v.x - ellipse.a, v.y - ellipse.b))
        else:
            pygame.draw.ellipse(self.s, color, rect, width)
