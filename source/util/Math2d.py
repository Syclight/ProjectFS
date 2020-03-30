class vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return '<Shape::{}({}, {})>'.format(self.__class__.__name__, self.x, self.y)

    def isZero(self):
        return self.x == 0 and self.y == 0

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
