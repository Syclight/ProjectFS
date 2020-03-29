from source.controller.assembly.IOEvent import IOEvent3, ElementHadDoEvent
from source.controller.dataStructure.QuadTree import RectangleRange, QuadTree, Node
from source.controller.assembly.Shape import Shape, Rectangle


class Actor:
    def __init__(self, texture, collideArea=None, physicalBodyType=None, visual=True, zIndex=0, frozen=False):
        self.Events = IOEvent3()
        self.EventsHadDo = ElementHadDoEvent()
        self.texture = texture
        self.visual = visual
        self.zIndex = zIndex
        self.physicalBodyType = physicalBodyType
        self.frozen = frozen
        self.collideArea = collideArea
        if not self.collideArea:
            x = self.texture.get_rect().x
            y = self.texture.get_rect().y
            w = self.texture.get_rect().w
            h = self.texture.get_rect().h
            self.collideArea = Rectangle(x, y, w, h)
        self.init_Rect = self.collideArea

    def collided(self, othActor):
        if not isinstance(othActor, Actor):
            raise Exception("Class '{}' must is a subclass of 'Actor'".format(othActor))
        return self.collideArea.intersects(othActor)

    def update(self):
        pass

    def draw(self, screen):
        pass


class ActorGroup:
    def __init__(self, activeArea, *args):
        self.actors = []
        for p in args:
            if not isinstance(p, Actor):
                raise Exception("Class '{}' must is a subclass of 'Actor'".format(p))
            self.actors.append(p)
        if not isinstance(activeArea, Shape):
            raise Exception("Class '{}' must is a subclass of 'Shape'".format(activeArea))
        self.activeArea = activeArea
        self.__activeArea = RectangleRange(activeArea.w / 2, activeArea.h / 2, activeArea.w / 2, activeArea.h / 2)
        self.__quadTree = QuadTree(self.__activeArea, 4)
        self.__collideDict = {}

    def add(self, *actors):
        for a in actors:
            if not isinstance(a, Actor):
                raise Exception("Class '{}' must is a subclass of 'Actor'".format(a))
            self.actors.append(a)

    def remove(self, actor):
        if actor in self.actors:
            self.actors.remove(actor)

    def size(self):
        return len(self.actors)

    def update(self):
        self.__quadTree = QuadTree(self.__activeArea, 4)
        self.__collideDict.clear()

        for a in self.actors:
            if not a.frozen:
                a.update()
                node = Node(a.collideArea.x, a.collideArea.y, a)
                self.__quadTree.insert(node)

    def draw(self, screen):
        for a in self.actors:
            if a.visual:
                a.draw(screen)

    def getCollideDict(self):
        for e in self.actors:
            _list = []
            _range = RectangleRange(e.collideArea.x, e.collideArea.y, e.collideArea.w * 2, e.collideArea.h * 2)
            sprites = self.__quadTree.query(_range)
            for _s in sprites:
                if e is not _s.data and e.collided(_s.data):
                    _list.append(_s.data)
            if _list:
                self.__collideDict[e] = _list
        return self.__collideDict

    def getCollideList(self, actor, isDel):
        _lis = []
        if not isinstance(actor, ActorGroup):
            raise Exception("Class '{}' must is a subclass of 'Actor'".format(actor))
        for a in self.actors:
            if a.collided(actor):
                _lis.append(a)
                if isDel:
                    self.remove(a)
        return _lis

    def getCollide_with_Oth(self, oth):
        raise Exception("function getCollide_with_Oth incompletely'")
        # if not isinstance(oth, ActorGroup):
        #     raise Exception("Class '{}' must is a subclass of 'ActorGroup'".format(oth))
        # if not self.activeArea.same(oth.activeArea):
        #     temp_new_area = Rectangle()
        # temp_group = ActorGroup(oth.activeArea, oth.actors)
        # temp_group.add(self.actors)



