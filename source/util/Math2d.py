import math


class vec2:
    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)

    def __str__(self):
        return '<vec2::{}({}, {})>'.format(self.__class__.__name__, self.x, self.y)

    def __add__(self, other):
        return vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return vec2(self.x - other.x, self.y - other.y)

    def copy(self):
        return vec2(self.x, self.y)

    def isZero(self):
        return self.x == 0.0 and self.y == 0.0

    def invert(self):
        x, y = 0, 0
        if self.x != 0:
            x = 1 / self.x
        if self.y != 0:
            y = 1 / self.y
        return vec2(x, y)

    def negate(self):
        return vec2(-self.x, -self.y)

    def same(self, shape) -> bool:
        if not isinstance(shape, vec2):
            return False
        return self.x == shape.x and self.y == shape.y

    def dist(self, _vec2=None):
        temp_vec2 = _vec2
        if temp_vec2 is None:
            temp_vec2 = vec2()
        return pow(pow((self.x - temp_vec2.x), 2) + pow((self.y - temp_vec2.y), 2), 0.5)

    def len_square(self):
        return self.x * self.x + self.y * self.y

    def mulNum(self, num):
        return vec2(self.x * num, self.y * num)

    def len(self):
        return pow(self.len_square(), 0.5)

    def dot(self, _vec2):
        return self.x * _vec2.x + self.y * _vec2.y

    def cross(self, _vec2):
        return self.x * _vec2.y - self.y * _vec2.x

    def normal(self):
        _len = self.len()
        if _len == 0:
            return vec2()
        return vec2(self.x / _len, self.y / _len)

    def angle_cos(self, _vec2):
        return self.dot(_vec2) / self.len() * _vec2.len()

    def angle(self, _vec2):
        return math.acos(self.angle_cos(_vec2))

    def rotate(self, angle):
        return vec2(self.x * math.cos(angle) - self.y * math.sin(angle),
                    self.x * math.sin(angle) + self.y * math.cos(angle))


class point2(vec2):
    def __init__(self, x, y):
        super(point2, self).__init__(x, y)

    def __str__(self):
        return '<point2::{}({}, {})>'.format(self.__class__.__name__, self.x, self.y)
