class Range:
    def contains(self, node):
        pass

    def intersects(self, oth):
        pass


class RectangleRange(Range):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def contains(self, point):
        return (self.x - self.w <= point.x <= self.x + self.w and
                self.y - self.h <= point.y <= self.y + self.h)

    def intersects(self, oth):
        return not (oth.x - oth.w > self.x + self.w or
                    oth.x + oth.w < self.x - self.w or
                    oth.y - oth.h > self.y + self.h or
                    oth.y + oth.h < self.y - self.h)


class CircleRange(Range):
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.squared_r = self.r * self.r

    def contains(self, point):
        d = pow((point.x - self.x), 2) + pow((point.y - self.y), 2)
        return d <= self.squared_r

    def intersects(self, oth):
        dist_x = abs(oth.x - self.x)
        dist_y = abs(oth.y - self.y)
        r = self.r
        w = oth.w
        h = oth.h
        edges = pow((dist_x - w), 2) + pow((dist_y - h), 2)

        if dist_x > (r + w) or dist_y > (r + h):
            return False
        if dist_x <= w or dist_y <= h:
            return True
        return edges <= self.squared_r


class Node:
    def __init__(self, x, y, data):
        self.x = x
        self.y = y
        self.data = data


class QuadTree:
    def __init__(self, boundary, capacity):
        if not isinstance(boundary, Range):
            raise Exception("'{}' must implement class 'QuadTree::Range'".format(boundary))

        self.boundary = boundary
        self.capacity = capacity
        self.points = []
        self.divided = False
        self.quadOne = None
        self.quadTwo = None
        self.quadThr = None
        self.quadFou = None

    def subdivide(self):
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w / 2
        h = self.boundary.h / 2

        self.quadOne = QuadTree(RectangleRange(x + w, y - h, w, h), self.capacity)
        self.quadTwo = QuadTree(RectangleRange(x - w, y - h, w, h), self.capacity)
        self.quadThr = QuadTree(RectangleRange(x + w, y + h, w, h), self.capacity)
        self.quadFou = QuadTree(RectangleRange(x - w, y + h, w, h), self.capacity)

        self.divided = True

    def insert(self, node):
        if not self.boundary.contains(node):
            return False
        if len(self.points) < self.capacity:
            self.points.append(node)
            return True
        if not self.divided:
            self.subdivide()
        return self.quadOne.insert(node) or self.quadTwo.insert(node) or self.quadThr.insert(
            node) or self.quadFou.insert(node)

    def query(self, _range, res=None):
        if not isinstance(_range, Range):
            raise Exception("'{}' must implement class 'QuadTree::Range'".format(_range))

        if res is None:
            res = []
        if not self.boundary.intersects(_range):
            return res

        for p in self.points:
            if _range.contains(p):
                res.append(p)
        if self.divided:
            self.quadOne.query(_range, res)
            self.quadTwo.query(_range, res)
            self.quadThr.query(_range, res)
            self.quadFou.query(_range, res)
        return res

    def length(self):
        count = len(self.points)
        if self.divided:
            count += self.quadOne.length()
            count += self.quadTwo.length()
            count += self.quadThr.length()
            count += self.quadFou.length()
        return count
