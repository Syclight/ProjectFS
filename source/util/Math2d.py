import math
import random

from source.util.MathConst import PI_DOUBLE


class vec2:
    """Math2d::vec2\n
    @overwrite: __str__, __add__, __sub__
    """

    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)

    def __str__(self):
        return '<vec2::{}({}, {})>'.format(self.__class__.__name__, self.x, self.y)

    def __add__(self, other):
        return vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return vec2(self.x - other.x, self.y - other.y)

    @staticmethod
    def fromAngle(angle, length=1):
        return vec2(length * math.cos(angle), length * math.sin(angle))

    @staticmethod
    def random(a=0, b=1):
        return vec2.fromAngle(random.uniform(a, b) * PI_DOUBLE)

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

    def same(self, *args) -> bool:
        if len(args) == 1:
            if not isinstance(args, vec2):
                return False
            return self.x == args.x and self.y == args.y
        else:
            _x, _y = args[0], args[1]
            return self.x == _x and self.y == _y

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

    def setLen(self, length):
        return self.normal().mulNum(length)

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


class dtm2:
    """Math2d::determinant2:
        |x1  y1|\n
        |x2  y2|
    @ rewrite __str__, __add__, __mul__, __truediv__\n
    @ method mul(Number) -> dtm2 : mul a number\n
    @ method val(None) -> float : the number value of the determinant2
    """

    def __init__(self, x1, y1, x2, y2):
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2

    def __str__(self):
        return '<dtm2::{}\n(|{}, {}|\n|{}, {}|)>'.format(self.__class__.__name__, self.x1, self.y1, self.x2, self.y2)

    def __add__(self, other):
        return self.val() + other.val()

    def __mul__(self, other):
        return self.val() * other.val()

    def __truediv__(self, other):
        return self.val() / other.val()

    def mul(self, num):
        return dtm2(self.x1 * num, self.y1 * num, self.x2, self.y2)

    def div(self, num):
        return dtm2(self.x1 / num, self.y1 / num, self.x2, self.y2)

    def val(self):
        return self.x1 * self.y2 - self.y1 * self.x2
