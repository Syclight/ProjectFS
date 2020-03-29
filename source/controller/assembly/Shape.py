from math import pi


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


class vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return '<Shape::{}({}, {})>'.format(self.__class__.__name__, self.x, self.y)

    def same(self, shape) -> bool:
        if not isinstance(shape, vec2):
            return False
        return self.x == shape.x and self.y == shape.y

    def dist(self, _vec2=None):
        temp_vec2 = _vec2
        if temp_vec2 is None:
            temp_vec2 = vec2(0, 0)
        return pow(pow((self.x - temp_vec2.x), 2) + pow((self.y - temp_vec2.y), 2), 0.5)


class Point2D(vec2):
    def __init__(self, x, y):
        super(Point2D, self).__init__(x, y)


class Triangle(Shape):
    def __init__(self, *vec):
        self.p1 = vec[0]
        self.p2 = vec[1]
        self.p3 = vec[2]

    def __str__(self):
        return '<Shape::{}({}, {}, {})>'.format(self.__class__.__name__, self.p1, self.p2, self.p3)

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
        self.center = Point2D(self.x + self.w / 2, self.y + self.h / 2)  # 重心坐标

    def __str__(self):
        return '<Shape::{}({}, {}, {}, {})>'.format(self.__class__.__name__, self.x, self.y, self.w, self.h)

    def contains(self, point) -> bool:
        return self.x + self.w > point.x > self.x and self.y < point.y < self.y + self.h

    def intersects(self, shape) -> bool:
        if not isinstance(shape, Rectangle):
            raise Exception("Param '{}' not a subclass of Shape::Rectangle".format(shape))

        dist_x = abs(self.center.x - shape.center.x)  # 重心位于x方向上的距离
        dist_y = abs(self.center.y - shape.center.y)  # 重心位于y方向上的距离

        sum_x = self.w + shape.w  # x方向上的边长之和
        sum_y = self.h + shape.h  # y方向上的边长之和

        if dist_x * 2 <= sum_x and dist_y * 2 <= sum_y:
            return True
        return False

    def same(self, shape) -> bool:
        if not isinstance(shape, Rectangle):
            return False
        return self.x == shape.x and self.y == shape.y and self.w == shape.w and self.h == shape.h

    def area(self):
        return self.w * self.h

    def girth(self):
        return (self.w + self.h) * 2


class Square(Rectangle):
    def __init__(self, x, y, w):
        super(Square, self).__init__(x, y, w, w)

    def __str__(self):
        return '<Shape::{}({}, {}, {})>'.format(self.__class__.__name__, self.x, self.y, self.w)


class Circle(Shape):
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.d = self.r * 2
        self.squared_r = self.r * self.r

    def __str__(self):
        return '<Shape::{}({}, {}, {})>'.format(self.__class__.__name__, self.x, self.y, self.r)

    def same(self, shape) -> bool:
        if not isinstance(shape, Circle):
            return False
        return self.x == shape.x and self.y == shape.y and self.r == shape.r

    def area(self):
        return pi * self.squared_r

    def girth(self):
        return pi * self.d


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
        else:
            raise Exception("Param '{}' not a subclass of Shape::Square".format(shape))
