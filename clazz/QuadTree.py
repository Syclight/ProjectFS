class Ranges:
    def contains(self, node):
        pass

    def intersects(self, oth):
        pass


class Node:
    def __init__(self, x, y, data):
        self.x = x
        self.y = y
        self.data = data


class Rectangle(Ranges):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def contains(self, node):
        return (self.x - self.w <= node.x <= self.x + self.w and
                self.y - self.h <= node.y <= self.y + self.h)

    def intersects(self, oth):
        return not (oth.x - oth.w > self.x + self.w or
                    oth.x + oth.w < self.x - self.w or
                    oth.y - oth.h > self.y + self.h or
                    oth.y + oth.h < self.y - self.h)


class QuadTree:
    def __init__(self, boundary, capacity):
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
        w = self.boundary.w
        h = self.boundary.h

        self.quadOne = QuadTree(Rectangle(x + w / 2, y - h / 2, w / 2, h / 2), self.capacity)
        self.quadTwo = QuadTree(Rectangle(x - w / 2, y - h / 2, w / 2, h / 2), self.capacity)
        self.quadThr = QuadTree(Rectangle(x + w / 2, y + h / 2, w / 2, h / 2), self.capacity)
        self.quadFou = QuadTree(Rectangle(x - w / 2, y + h / 2, w / 2, h / 2), self.capacity)

        self.divided = True

    def insert(self, node):
        if self.boundary.contains(node):
            return False
        if len(self.points) < self.capacity:
            self.points.append(node)
            return True
        else:
            if not self.divided:
                self.subdivide()
            elif self.quadOne.insert(node):
                return True
            elif self.quadTwo.insert(node):
                return True
            elif self.quadThr.insert(node):
                return True
            elif self.quadFou.insert(node):
                return True

    def query(self, ranges, res=None):
        if res is None:
            res = []
        if not self.boundary.intersects(ranges):
            return res
        else:
            for p in self.points:
                if ranges.contains(p):
                    res.append(p)
            if self.divided:
                self.quadOne.query(ranges, res)
                self.quadTwo.query(ranges, res)
                self.quadThr.query(ranges, res)
                self.quadFou.query(ranges, res)
            return res
