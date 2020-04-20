import pygame

from source.controller.assembly.PhysicalBody import rigidBody, physicalScene, BodyType
from source.core.math.Vector import vec2
from source.core.math.Shape import Rectangle
from source.util.ToolsFuc import ex_toRect
from source.view.baseClazz.Actor import Actor
from source.view.baseClazz.Scene import Scene


class wallActor(Actor):
    def __init__(self, texture, rect=None):
        super(wallActor, self).__init__(texture, rect)

    def draw(self, screen):
        screen.blit(self.texture, ex_toRect(self.area))


class containerActor(Actor):
    def __init__(self, texture, rect=None):
        super(containerActor, self).__init__(texture, rect)
        self.physicalBody = rigidBody(1, self.area, BodyType.DYNAMIC)
        self.physicalBody.drag = vec2(0, 0)
        self.physicalBody.hasCollidedProbe = True
        self.physicalBody.restitution = 0.8

    def update(self):
        self.area = self.physicalBody.collideArea

    def draw(self, screen):
        screen.blit(self.texture, ex_toRect(self.area))


class ActorScene(Scene):
    def __init__(self, screen, config, clock):
        super(ActorScene, self).__init__(screen, config, clock)
        rect_container = Rectangle(600, 200, 100, 100)
        rect_container2 = Rectangle(600, 0, 100, 100)
        rect_container3 = Rectangle(0, 0, 100, 100)
        rect_container4 = Rectangle(400, 200, 100, 100)
        rect_wall = Rectangle(0, 200, 400, 400)

        self.__A_wall = wallActor(pygame.image.load('F:/练习/PyCharm/PygameTest/resource/Test/wall.jpg'), rect_wall)
        self.__A_container = containerActor(pygame.image.load('F:/练习/PyCharm/PygameTest/resource/Test/container1.jpg'),
                                            rect_container)
        self.__A_container2 = containerActor(pygame.image.load('F:/练习/PyCharm/PygameTest/resource/Test/container2.jpg'),
                                             rect_container2)
        self.__A_container3 = containerActor(pygame.image.load('F:/练习/PyCharm/PygameTest/resource/Test/container3.jpg'),
                                             rect_container3)
        self.__A_container4 = containerActor(pygame.image.load('F:/练习/PyCharm/PygameTest/resource/Test/container4.jpg'),
                                             rect_container4)
        self.__A_container2.physicalBody.vel = vec2(0, 3)
        self.__A_container3.physicalBody.vel = vec2(0, 3)
        self.ps = physicalScene(Rectangle(0, 0, 800, 600), vec2(0, 0.098), self.startClock)
        self.ps.add(self.__A_container.physicalBody)
        self.ps.add(self.__A_container2.physicalBody)
        self.ps.add(self.__A_container3.physicalBody)
        self.ps.add(self.__A_container4.physicalBody)

    def draw(self):
        # self.__A_wall.draw(self.screen)
        self.__A_container.draw(self.screen)
        self.__A_container2.draw(self.screen)
        self.__A_container3.draw(self.screen)
        self.__A_container4.draw(self.screen)

    def doClockEvent(self, NowClock):
        self.ps.update(NowClock)
        self.__A_wall.update()
