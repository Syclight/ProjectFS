import pygame

from source.controller.assembly.PhysicalBody import rigidBody
from source.controller.assembly.Shape import Rectangle
from source.util.ToolsFuc import ex_toRect
from source.view.baseClazz.Actor import Actor
from source.view.baseClazz.Scene import Scene


class wallActor(Actor):
    def __init__(self, texture, rect=None):
        super(wallActor, self).__init__(texture, rect)

    def draw(self, screen):
        screen.blit(self.texture, ex_toRect(self.collideArea))


class containerActor(Actor):
    def __init__(self, texture, rect=None):
        super(containerActor, self).__init__(texture, rect)

    def draw(self, screen):
        screen.blit(self.texture, ex_toRect(self.collideArea))


class ActorScene(Scene):
    def __init__(self, screen, config):
        super(ActorScene, self).__init__(screen, config)
        rect_container = Rectangle(600, 100, 100, 100)
        rect_wall = Rectangle(0, 200, 400, 400)
        self.__A_wall = wallActor(pygame.image.load('F:/练习/PyCharm/PygameTest/resource/Test/wall.jpg'), rect_wall)
        self.__A_container = containerActor(pygame.image.load('F:/练习/PyCharm/PygameTest/resource/Test/container.jpg'),
                                            rect_container)

    def draw(self):
        self.__A_wall.draw(self.screen)
        self.__A_container.draw(self.screen)
