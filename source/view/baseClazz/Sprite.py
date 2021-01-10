import pygame

from source.core.assembly.IOEvent import IOEvent3, ElementHadDoEvent
from source.core.dataStructure.QuadTree import QuadTree, Node, RectangleRange
from source.core.math.Shape import Rectangle


class Sprite(pygame.sprite.Sprite):
    """游戏中所有精灵的父类 框架：Syclight Framework with pygame

        实现自pygame.sprite.Sprite(*groups):

        在本框架中的声明精灵时要求继承该类，否则将会导致出错

        当继承该类时，要求使用该类的变量和实现必要的方法，用不到的方法可以忽略

        """

    def __init__(self, image, rect=None, isScale=True):
        super().__init__()
        self.image = image
        self.rect = rect
        if isinstance(rect, list) or isinstance(rect, tuple):
            self.rect = pygame.Rect(rect[0], rect[1], rect[2], rect[3])
        elif isinstance(rect, Rectangle):
            self.rect = pygame.Rect(rect.x, rect.y, rect.w, rect.h)
        if isinstance(self.image, str):
            self.image = pygame.image.load(image)
        if self.rect is None:
            self.rect = self.image.get_rect()
        elif isScale:
            self.image = pygame.transform.scale(self.image, (self.rect.w, self.rect.h))

        self.Events = IOEvent3()
        self.EventsHadDo = ElementHadDoEvent()
        self.visual = True
        self.active = True
        self.zIndex = 0
        self.physicalBodyType = None
        if isinstance(rect, tuple):
            self.collidedArea = Rectangle(self.rect[0], self.rect[1], self.rect[2], self.rect[3])
        else:
            self.collidedArea = Rectangle(self.rect.x, self.rect.y, self.rect.w, self.rect.h)

    def setRect(self, rec):
        if (isinstance(rec, tuple) or isinstance(rec, list)) and len(rec) >= 4:
            self.rect = pygame.Rect(rec[0], rec[1], rec[2], rec[3])
        else:
            self.rect = rec
        self.image = pygame.transform.scale(self.image, (self.rect.w, self.rect.h))
        self.collidedArea = Rectangle(self.rect.x, self.rect.y, self.rect.w, self.rect.h)

    def setImg(self, arg):
        if isinstance(arg, str):
            self.image = pygame.image.load(arg)
        if isinstance(arg, pygame.Surface):
            self.image = arg

    def draw(self, surface):
        if self.image:
            surface.blit(self.image, self.rect)

    def collided(self, oth):
        if not isinstance(oth, Sprite):
            raise Exception("Param '{}' must is a subclass of 'Sprite'".format(oth))
        if self.zIndex != oth.zIndex:
            return False
        return self.collidedArea.intersects(oth.collidedArea)


class SpriteGroup(pygame.sprite.Group):
    """游戏中所有精灵的精灵组 框架：Syclight Framework with pygame

            实现自pygame.sprite.Group:

            所有的精灵在建立精灵组时不一定要实现该类

            主要是弥补pygame没有精灵组组内检测碰撞的方法，组内碰撞采用四叉树

            注意：重写了pygame.sprite.Group的update方法和draw方法，主要是因为Sprite类中的draw方法
            如果不重写会在draw时会产生一些莫名其妙的bug

            """

    def __init__(self, activeArea, *sprites):
        super(SpriteGroup, self).__init__(*sprites)
        # if not hasattr(activeArea, 'w'):
        #     raise Exception("Class '{}' must have attribute 'w'".format(activeArea))
        # if not hasattr(activeArea, 'h'):
        #     raise Exception("Class '{}' must have attribute 'h'".format(activeArea))
        if isinstance(activeArea, list) or isinstance(activeArea, tuple):
            self.__activeArea = RectangleRange((activeArea[2] + activeArea[0]) / 2, (activeArea[3] - activeArea[1]) / 2,
                                               activeArea[2] / 2, activeArea[3] / 2)
        else:
            self.__activeArea = RectangleRange((activeArea.w + activeArea.x) / 2, (activeArea.h + activeArea.y) / 2,
                                               activeArea.w / 2, activeArea.h / 2)

        self.__quadTree = QuadTree(self.__activeArea, 4)
        self.__collideDict = {}

    def update(self, *args):
        self.__quadTree = QuadTree(self.__activeArea, 4)
        self.__collideDict.clear()

        for s in self.sprites():
            s.update(*args)
            node = Node(s.rect.x, s.rect.y, s)
            self.__quadTree.insert(node)

    def draw(self, surface):
        for s in self.sprites():
            s.draw(surface)

    def getCollideDict(self):
        for e in self.sprites():
            _list = []
            _range = RectangleRange(e.rect.x, e.rect.y, e.rect.w * 2, e.rect.h * 2)
            sprites = self.__quadTree.query(_range)
            for _s in sprites:
                if e is not _s.data and e.collided(_s.data):
                    _list.append(_s.data)
            if _list:
                self.__collideDict[e] = _list
        return self.__collideDict
