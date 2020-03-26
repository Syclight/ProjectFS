class vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Triangle:
    def __init__(self, vec):
        self.point1 = vec[0]
        self.point2 = vec[1]
        self.point3 = vec[2]


class Square:
    def __init__(self, l, t, w):
        self.l = l
        self.t = t
        self.w = w


class Circular:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r


# 内接圆
class InscribedCircular(Circular):
    def __init__(self, shape):
        if isinstance(shape, Square):
            r = shape.w / 2
            x = shape.l + r
            y = shape.t + r
            super(InscribedCircular, self).__init__(x, y, r)
        else:
            raise Exception("Param 'shape' not a subclass of Shape.Square")


# 外接圆
class CircumscribedCircle(Circular):
    def __init__(self, shape):
        if isinstance(shape, Square):
            x = shape.l + shape.w / 2
            y = shape.t + x
            r = pow(pow(x, 2) * 2, 0.5)
            super(CircumscribedCircle, self).__init__(x, y, r)
        else:
            raise Exception("Param 'shape' not a subclass of Shape.Square")
