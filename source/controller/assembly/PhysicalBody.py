from source.controller.assembly.CollidedProbe import CollidedProbe
from source.controller.assembly.Shape import Shape, Rectangle, Circle, Triangle, CircumscribedCircle
from source.controller.dataStructure.QuadTree import RectangleRange, QuadTree, Node, CircleRange
from source.util.Math2d import vec2


class BodyType:
    DYNAMIC = 0xA0001
    STATIC = 0xA0002

    RIGIDBODY = 0xB0001
    ELASTOMER = 0xB0002


class physicalBody:
    def __init__(self, mass=0, pos=vec2()):
        self.mass = mass
        self.vel = vec2()
        self.acc = vec2()
        self.pos = pos
        self.bodyType = 0
        self.drag = vec2()
        self.angularDrag = vec2()
        self.active = True
        self.isCollideChecked = False
        self.hasCollidedProbe = False

    def update(self, restrictedArea, unitTime):
        pass


class physicalScene:
    def __init__(self, activeArea, gravityAc, initTime):
        self.__bodies = []

        if not isinstance(activeArea, Shape):
            raise Exception("Class '{}' must is a subclass of 'Shape::Shape'".format(activeArea))
        self.activeArea = activeArea

        if not isinstance(gravityAc, vec2):
            raise Exception("Class '{}' must is a subclass of 'Math2D::vec2'".format(gravityAc))
        self.gravityAc = gravityAc

        self.__right = self.activeArea.right()
        self.__bottom = self.activeArea.bottom()
        self.__left = self.activeArea.left()
        self.__top = self.activeArea.top()

        self.__initTime = initTime
        self.__unitTime = 4  # 0.0033sce
        self.__interval = 0

        self.__collidedProbe = CollidedProbe()

        self.__activeRange = RectangleRange(activeArea.w / 2, activeArea.h / 2, activeArea.w / 2, activeArea.h / 2)
        self.__quadTree = QuadTree(self.__activeRange, 4)

    def add(self, *args):
        for a in args:
            if not isinstance(a, physicalBody):
                raise Exception("Class '{}' must is a subclass of 'Actor'".format(a))
            self.__bodies.append(a)

    def remove(self, e):
        if e in self.__bodies:
            self.__bodies.remove(e)

    def size(self):
        return len(self.__bodies)

    def update(self, nowTime):

        self.__initTime = nowTime
        self.__quadTree = QuadTree(self.__activeRange, 4)

        for a in self.__bodies:
            if a.active:
                gravity = self.gravityAc.mulNum(a.mass)
                a.applyForce(gravity)
                a.update(self.activeArea, self.__unitTime)
                if a.collideArea.right() > self.__right:
                    a.collideArea.x = self.__right
                    a.vel.x *= -a.restitution
                if a.collideArea.bottom() > self.__bottom:
                    a.collideArea.y = self.__bottom - a.collideArea.h
                    a.vel.y *= -a.restitution
                if a.collideArea.left() < self.__left:
                    a.collideArea.x = self.__left
                    a.vel.x *= -a.restitution
                if a.collideArea.top() < self.__top:
                    a.collideArea.y = self.__top + a.collideArea.h
                    a.vel.y *= -a.restitution
                a.isCollideChecked = False
            node = Node(a.collideArea.x, a.collideArea.y, a)
            self.__quadTree.insert(node)

        for e in self.__bodies:
            sprites = self.__quadTree.query(
                RectangleRange(e.collideArea.x, e.collideArea.y, e.collideArea.w, e.collideArea.h))
            for _s in sprites:
                if e is not _s.data and e.collided(_s.data):
                    if e.hasCollidedProbe and not e.isCollideChecked:
                        self.__collidedProbe.execute(e, _s.data, self.__unitTime)
                        e.isCollideChecked = True
                        _s.data.isCollideChecked = True


class rigidBody(physicalBody):
    def __init__(self, mass, collideArea, _type):
        super(rigidBody, self).__init__(mass, collideArea.barycenter())
        self.bodyType = BodyType.RIGIDBODY | _type
        self.collideArea = collideArea
        self.density = 1
        self.friction = 0.1
        self.restitution = 1

    def applyForce(self, force):
        f = force.mulNum(1 / self.mass)
        self.acc += f

    def dis_bary(self):
        x1 = self.collideArea.right() - self.pos.x
        x2 = self.pos.x - self.collideArea.left()
        y1 = self.collideArea.bottom() - self.pos.y
        y2 = self.pos.y - self.collideArea.top()
        return x1, x2, y1, y2

    def collided(self, oth):
        return self.collideArea.intersects(oth.collideArea)

    def update(self, restrictedArea, unitTime):
        self.vel += self.acc
        self.pos += self.vel
        self.acc = self.acc.mulNum(0)

        self.collideArea.rebuildForBarycenter(self.pos)
