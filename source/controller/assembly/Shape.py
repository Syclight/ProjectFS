from math import pi

from source.util.Math2d import point2, vec2, dtm2


class Shape:
    def contains(self, point) -> bool:
        pass

    def intersects(self, shape) -> bool:
        pass

    def same(self, shape) -> bool:
        pass

    def area(self):
        pass

    def girth(self):
        pass

    def left(self):
        pass

    def right(self):
        pass

    def top(self):
        pass

    def bottom(self):
        pass

    def barycenter(self):
        pass

    def doubleRange(self):
        pass

    def rebuildForBarycenter(self, point):
        pass


class Line(Shape):
    def __init__(self, pos, angle, length=0):
        self.pos = pos
        self.dir = vec2.fromAngle(angle)
        self.length = length

    def setAngle(self, angle):
        self.dir = vec2.fromAngle(angle)

    def cast(self, a, b):
        x1 = a.x
        y1 = a.y
        x2 = b.x
        y2 = b.y

        x3 = self.pos.x
        y3 = self.pos.y
        x4 = self.pos.x + self.dir.x
        y4 = self.pos.y + self.dir.y
        dt = dtm2(x1 - x3, x3 - x4, y1 - y3, y3 - y4)
        du = dtm2(x1 - x2, x1 - x3, y1 - y2, y1 - y3)
        dd = dtm2(x1 - x2, x3 - x4, y1 - y2, y3 - y4)
        dd_val = dd.val()

        if dd_val == 0:
            return

        t = dt.val() / dd_val
        u = du.val() / dd_val

        if 0 < t < 1 and u > 0:
            return vec2(x1 + t * (x2 - x1), y1 + t * (y2 - y1))
        else:
            return


class Triangle(Shape):
    def __init__(self, *vec):
        self.p1 = vec[0]
        self.p2 = vec[1]
        self.p3 = vec[2]

    def __str__(self):
        return '<Shape::{}({}, {}, {})>'.format(self.__class__.__name__, self.p1, self.p2, self.p3)

    def barycenter(self):
        return point2((self.p1.x + self.p2.x + self.p3.x) / 3, (self.p1.y + self.p2.y + self.p3.y) / 3)

    def same(self, shape) -> bool:
        if not isinstance(shape, Triangle):
            return False
        return self.p1 == shape.p1 and self.p2 == shape.p2 and self.p3 == shape.p3


class Rectangle(Shape):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def __str__(self):
        return '<Shape::{}({}, {}, {}, {})>'.format(self.__class__.__name__, self.x, self.y, self.w, self.h)

    def contains(self, point) -> bool:
        return self.x + self.w > point.x > self.x and self.y < point.y < self.y + self.h

    def intersects(self, shape) -> bool:
        if not isinstance(shape, Rectangle):
            raise Exception("Param '{}' not a subclass of Shape::Rectangle".format(shape))
        center1 = self.barycenter()
        center2 = shape.barycenter()

        dist_x = abs(center1.x - center2.x)  # 重心位于x方向上的距离
        dist_y = abs(center1.y - center2.y)  # 重心位于y方向上的距离

        sum_x = self.w + shape.w  # x方向上的边长之和
        sum_y = self.h + shape.h  # y方向上的边长之和

        if dist_x * 2 <= sum_x and dist_y * 2 <= sum_y:
            return True
        return False

    def same(self, shape) -> bool:
        if not isinstance(shape, Rectangle):
            return False
        return self.x == shape.x and self.y == shape.y and self.w == shape.w and self.h == shape.h

    def array(self):
        p1, p2 = point2(self.x, self.y), point2(self.x + self.w, self.y)
        p4, p3 = point2(self.x, self.y + self.h), point2(self.x + self.w, self.y + self.h)
        return [p1, p2, p3, p4]

    def area(self):
        return self.w * self.h

    def girth(self):
        return (self.w + self.h) * 2

    def left(self):
        return self.x

    def right(self):
        return self.x + self.w

    def top(self):
        return self.y

    def bottom(self):
        return self.y + self.h

    def barycenter(self):
        return point2(self.x + self.w / 2, self.y + self.h / 2)

    def doubleRange(self):
        return self.x, self.y, self.w * 2, self.h * 2

    def rebuildForBarycenter(self, point):
        self.x = point.x - self.w / 2
        self.y = point.y - self.h / 2


class Square(Rectangle):
    def __init__(self, x, y, w):
        super(Square, self).__init__(x, y, w, w)

    def __str__(self):
        return '<Shape::{}({}, {}, {})>'.format(self.__class__.__name__, self.x, self.y, self.w)


class Ellipse(Shape):
    def __init__(self, x, y, a, b):
        self.x = x
        self.y = y
        self.a = a
        self.b = b

    def __str__(self):
        return '<Shape::{}({}, {}, {}, {})>'.format(self.__class__.__name__, self.x, self.y, self.a, self.b)

    def same(self, shape) -> bool:
        if not isinstance(shape, Ellipse):
            return False
        return self.x == shape.x and self.y == shape.y and self.a == shape.a and self.b == shape.b

    def barycenter(self):
        return point2(self.x, self.y)

    def area(self):
        return pi * self.a * self.b

    def doubleRange(self):
        return self.x, self.y, self.a * 2, self.b * 2


class Circle(Shape):
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    def __str__(self):
        return '<Shape::{}({}, {}, {})>'.format(self.__class__.__name__, self.x, self.y, self.r)

    def same(self, shape) -> bool:
        if not isinstance(shape, Circle):
            return False
        return self.x == shape.x and self.y == shape.y and self.r == shape.r

    def barycenter(self):
        return point2(self.x, self.y)

    def area(self):
        return pi * self.r * self.r

    def doubleRange(self):
        return self.x, self.y, self.r * 2

    def girth(self):
        return pi * self.r * 2

    # 内接圆


class InscribedCircle(Circle):
    def __init__(self, shape):
        if isinstance(shape, Square):
            r = shape.w / 2
            x = shape.x + r
            y = shape.y + r
            super(InscribedCircle, self).__init__(x, y, r)
        else:
            raise Exception("Param '{}' not a subclass of Shape::Square".format(shape))


# 外接圆
class CircumscribedCircle(Circle):
    def __init__(self, shape):
        if isinstance(shape, Square):
            w = shape.w / 2
            x = shape.x + w
            y = shape.y + w
            r = pow(pow(w, 2) * 2, 0.5)
            super(CircumscribedCircle, self).__init__(x, y, r)
        elif isinstance(shape, Rectangle):
            p = shape.barycenter()
            x = p.x
            y = p.y
            r = pow(pow(shape.w, 2) + pow(shape.h, 2), 0.5) / 2
            super(CircumscribedCircle, self).__init__(x, y, r)
        else:
            raise Exception("Param '{}' not a subclass of Shape::Square".format(shape))
