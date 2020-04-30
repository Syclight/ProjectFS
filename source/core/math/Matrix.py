from source.core.math.Vector import vec3


class dtm2:
    """determinant_2x2:
        |x1  y1|\n
        |x2  y2|
    @ rewrite __str__, __add__, __mul__, __truediv__\n
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


class mat3:
    """matrix_3x3:
            |m0  m1  m2|\n
            |m3  m4  m5|\n
            |m6  m7  m8|
        @ rewrite __str__, __add__, __mul__, __truediv__\n
        """

    def __init__(self, *args):
        self.m = [0] * 9
        if len(args) == 3:
            if isinstance(args[0], vec3):
                self.m[0], self.m[1], self.m[2] = args[0].x, args[0].y, args[0].z
                self.m[3], self.m[4], self.m[5] = args[1].x, args[1].y, args[1].z
                self.m[6], self.m[7], self.m[8] = args[2].x, args[2].y, args[2].z
            elif isinstance(args[0], tuple) or isinstance(args[0], list):
                self.m[0], self.m[1], self.m[2] = args[0][0], args[0][1], args[0][2]
                self.m[3], self.m[4], self.m[5] = args[1][0], args[1][1], args[1][2]
                self.m[6], self.m[7], self.m[8] = args[2][0], args[2][1], args[2][2]
        elif len(args) == 9:
            self.m[0], self.m[1], self.m[2] = args[0], args[1], args[2]
            self.m[3], self.m[4], self.m[5] = args[3], args[4], args[5]
            self.m[6], self.m[7], self.m[8] = args[6], args[7], args[8]
        else:
            self.m[0], self.m[1], self.m[2] = 1, 0, 0
            self.m[3], self.m[4], self.m[5] = 0, 1, 0
            self.m[6], self.m[7], self.m[8] = 0, 0, 1

    def __add__(self, other):
        return mat3(
            self.m[0] + other.m[0], self.m[1] + other.m[1], self.m[2] + other.m[2],
            self.m[3] + other.m[3], self.m[4] + other.m[4], self.m[5] + other.m[5],
            self.m[6] + other.m[6], self.m[7] + other.m[7], self.m[8] + other.m[8]
        )

    def __sub__(self, other):
        return mat3(
            self.m[0] - other.m[0], self.m[1] - other.m[1], self.m[2] - other.m[2],
            self.m[3] - other.m[3], self.m[4] - other.m[4], self.m[5] - other.m[5],
            self.m[6] - other.m[6], self.m[7] - other.m[7], self.m[8] - other.m[8]
        )

    def __mul__(self, other):
        return mat3(
            self.m[0] * other.m[0] + self.m[1] * other.m[3] + self.m[2] * other.m[6],
            self.m[0] * other.m[1] + self.m[1] * other.m[4] + self.m[2] * other.m[7],
            self.m[0] * other.m[2] + self.m[1] * other.m[5] + self.m[2] * other.m[8],
            self.m[3] * other.m[0] + self.m[4] * other.m[3] + self.m[5] * other.m[6],
            self.m[3] * other.m[1] + self.m[4] * other.m[4] + self.m[5] * other.m[7],
            self.m[3] * other.m[2] + self.m[4] * other.m[5] + self.m[5] * other.m[8],
            self.m[6] * other.m[0] + self.m[7] * other.m[3] + self.m[8] * other.m[6],
            self.m[6] * other.m[1] + self.m[7] * other.m[4] + self.m[8] * other.m[7],
            self.m[6] * other.m[2] + self.m[7] * other.m[5] + self.m[8] * other.m[8]
        )

    def __truediv__(self, other):
        pass

    def __getitem__(self, item):
        index = item * 3
        return [self.m[index], self.m[index + 1], self.m[index + 2]]

    def __setitem__(self, key, value):
        index = key * 3
        self.m[index], self.m[index + 1], self.m[index + 2] = value

    def __str__(self):
        return '<mat3::{}([{}, {}, {}][{}, {}, {}][{}, {}, {}])>'.format(
            self.__class__.__name__,
            self.m[0], self.m[1], self.m[2],
            self.m[3], self.m[4], self.m[5],
            self.m[6], self.m[7], self.m[8])

    @staticmethod
    def isZero_(mat):
        for n in mat.m:
            if n != 0:
                return False
        return True

    def set(self, row, col, val):
        self.m[col + row * 3] = val

    def copy(self):
        return mat3(self.m[0], self.m[1], self.m[2],
                    self.m[3], self.m[4], self.m[5],
                    self.m[6], self.m[7], self.m[8])

    def trans(self):
        return mat3(
            self.m[0], self.m[3], self.m[6],
            self.m[1], self.m[4], self.m[7],
            self.m[2], self.m[5], self.m[8]
        )

    def mul_vec3(self, v):
        return vec3(
            self.m[0] * v.x + self.m[1] * v.y + self.m[2] * v.z,
            self.m[3] * v.x + self.m[4] * v.y + self.m[5] * v.z,
            self.m[6] * v.x + self.m[7] * v.y + self.m[8] * v.z,
        )
