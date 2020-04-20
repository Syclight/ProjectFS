import math
import random

from source.core.math.MathConst import PI_DOUBLE


class vec2:
    """Vector::vec2\n
    @overwrite: __str__, __add__, __sub__
    """

    def __init__(self, x=0.0, y=0.0):
        if isinstance(x, tuple) or isinstance(x, list):
            self.__init__(x[0], x[1])
        else:
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

    @staticmethod
    def lerp_between(v1, v2, amt):
        tar = v1.copy()
        return tar.lerp(v2, amt)

    def orient(self):
        return math.atan2(self.y, self.x)

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
            _v = args[0]
            if not isinstance(_v, vec2):
                return False
            return self.x == _v.x and self.y == _v.y
        else:
            if len(args) != 2:
                return False
            _x, _y = args[0], args[1]
            return self.x == _x and self.y == _y

    def dist(self, _vec2=None):
        temp_vec2 = _vec2
        if temp_vec2 is None:
            temp_vec2 = vec2()
        return pow(pow((self.x - temp_vec2.x), 2) + pow((self.y - temp_vec2.y), 2), 0.5)

    def len_square(self):
        return self.x * self.x + self.y * self.y

    def mul(self, num):
        return vec2(self.x * num, self.y * num)

    def dev(self, num):
        return vec2(self.x / num, self.y / num)

    def len(self):
        return pow(self.len_square(), 0.5)

    def setLen(self, length):
        v = self.normal().mul(length)
        self.x, self.y = v.x, v.y
        return self

    def dot(self, _vec2):
        return self.x * _vec2.x + self.y * _vec2.y

    def cross(self, _vec2):
        return self.x * _vec2.y - self.y * _vec2.x

    def normal(self):
        _len = self.len()
        if _len == 0:
            return vec2()
        return vec2(self.x / _len, self.y / _len)

    def limit(self, n):
        v = vec2(self.x, self.y)
        len_sq = self.len_square()
        if len_sq > n * n:
            v = v.dev(math.sqrt(len_sq)).mul(n)
        self.x, self.y = v.x, v.y
        return self

    def reflect(self, normal):
        normal.normal()
        return self - normal * (2 * self.dot(normal))

    def lerp(self, x, y, amt=0):
        if isinstance(x, vec2):
            self.lerp(x.x, x.y, y)
        else:
            self.x += (x - self.x) * amt or 0
            self.y += (y - self.y) * amt or 0
        return self

    def angle_cos(self, _vec2):
        return self.dot(_vec2) / (self.len() * _vec2.len())

    def angle(self, _vec2):
        return math.acos(min(1, max(-1, self.angle_cos(_vec2))))

    def rotate(self, angle):
        return vec2(self.x * math.cos(angle) - self.y * math.sin(angle),
                    self.x * math.sin(angle) + self.y * math.cos(angle))

    def ary(self):
        return self.x, self.y


class point2(vec2):
    def __init__(self, x=0, y=0):
        super(point2, self).__init__(x, y)

    def __str__(self):
        return '<point2::{}({}, {})>'.format(self.__class__.__name__, self.x, self.y)


class vec3:
    """Vector::vec3\n
    @overwrite: __str__, __add__, __sub__
    """

    def __init__(self, x=0.0, y=0.0, z=0.0):
        if isinstance(x, tuple) or isinstance(x, list):
            self.__init__(x[0], x[1], x[2])
        else:
            self.x = float(x)
            self.y = float(y)
            self.z = float(z)

    def __str__(self):
        return '<vec3::{}({}, {}, {})>'.format(self.__class__.__name__, self.x, self.y, self.z)

    def __add__(self, other):
        return vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    @staticmethod
    def fromAngle(theta, phi, length=1):
        """theta: number 极角(极坐标， 0，向上)

        phi: number 方位角(0, 屏幕外)
        """
        cosPhi = math.cos(phi)
        sinPhi = math.sin(phi)
        cosTheta = math.cos(theta)
        sinTheta = math.sin(theta)

        return vec3(length * sinTheta * sinPhi, -length * cosTheta, length * sinTheta * cosPhi)

    @staticmethod
    def random(a=0, b=1):
        angle = random.uniform(a, b) * PI_DOUBLE;
        vz = random.uniform(a, b) * 2 - 1
        vzBase = math.sqrt(1 - vz * vz)
        vx = vzBase * math.cos(angle)
        vy = vzBase * math.sin(angle)
        return vec3(vx, vy, vz)

    @staticmethod
    def lerp_between(v1, v2, amt):
        tar = v1.copy()
        return tar.lerp(v2, amt)

    def copy(self):
        return vec3(self.x, self.y, self.z)

    def isZero(self):
        return self.x == 0.0 and self.y == 0.0 and self.z == 0

    def invert(self):
        x, y, z = 0, 0, 0
        if self.x != 0:
            x = 1 / self.x
        if self.y != 0:
            y = 1 / self.y
        if self.z != 0:
            z = 1 / self.z
        return vec3(x, y, z)

    def orient(self):
        return math.atan2(self.y, self.x)

    def negate(self):
        return vec3(-self.x, -self.y, -self.z)

    def same(self, *args) -> bool:
        if len(args) == 1:
            _v = args[0]
            if not isinstance(_v, vec3):
                return False
            return self.x == _v.x and self.y == _v.y and self.z == _v.z
        else:
            if len(args) != 3:
                return False
            _x, _y, _z = args[0], args[1], args[2]
            return self.x == _x and self.y == _y

    def dist(self, _vec3=None):
        temp_vec3 = _vec3
        if temp_vec3 is None:
            temp_vec3 = vec3()
        return pow(pow((self.x - temp_vec3.x), 2) + pow((self.y - temp_vec3.y), 2) + pow((self.z - temp_vec3.z), 2),
                   0.5)

    def len_square(self):
        return self.x * self.x + self.y * self.y + self.z * self.z

    def mul(self, num):
        return vec3(self.x * num, self.y * num, self.z * num)

    def dev(self, num):
        return vec3(self.x / num, self.y / num, self.z / num)

    def len(self):
        return pow(self.len_square(), 0.5)

    def setLen(self, length):
        v = self.normal().mul(length)
        self.x, self.y, self.z = v.x, v.y, v.z
        return self

    def dot(self, _vec3):
        return self.x * _vec3.x + self.y * _vec3.y + self.z * _vec3.z

    def cross(self, _vec3):
        return vec3(self.y * _vec3.z - self.z * _vec3.y, self.z * _vec3.x - self.x * _vec3.z,
                    self.x * _vec3.y - self.y * _vec3.x)

    def normal(self):
        _len = self.len()
        if _len == 0:
            return vec3()
        return vec3(self.x / _len, self.y / _len, self.z / _len)

    def limit(self, n):
        v = vec3(self.x, self.y, self.z)
        len_sq = self.len_square()
        if len_sq > n * n:
            v = v.dev(math.sqrt(len_sq)).mul(n)
        self.x, self.y, self.z = v.x, v.y, v.z
        return self

    def reflect(self, normal):
        normal.normal()
        return self - normal * (2 * self.dot(normal))

    def lerp(self, x, y, z, amt=0):
        if isinstance(x, vec3):
            self.lerp(x.x, x.y, x.z, y)
        else:
            self.x += (x - self.x) * amt or 0
            self.y += (y - self.y) * amt or 0
            self.z += (z - self.z) * amt or 0
        return self

    def angle_cos(self, _vec3):
        return self.dot(_vec3) / (self.len() * _vec3.len())

    def angle(self, _vec2):
        return math.acos(min(1, max(-1, self.angle_cos(_vec2))))

    def rotate(self, angle, _vec3):
        """_vec3: vec3 旋转向量"""
        v = self.copy()
        return v.mul(math.cos(angle)) + (1 - math.cos(angle)) * (self.dot(_vec3)) * _vec3 + v.cross(_vec3).mul(
            math.sin(angle))

    def ary(self):
        return self.x, self.y, self.z
