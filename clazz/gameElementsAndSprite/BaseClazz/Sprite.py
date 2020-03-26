import pygame

from clazz.Element import ElementHadDoEvent
from clazz.IOEvent import IOEvent3
from model.Shape import Square, InscribedCircular, CircumscribedCircle


class Sprite(pygame.sprite.Sprite):
    """游戏中所有精灵的父类 框架：Syclight Framework with pygame

        实现自pygame.sprite.Sprite(*groups):

        在本框架中的声明精灵时要求继承该类，否则将会导致出错

        当继承该类时，要求使用该类的变量和实现必要的方法，用不到的方法可以忽略

        """

    def __init__(self, imagePath, areaType=0):
        super().__init__()
        self.image = pygame.image.load(imagePath)
        self.rect = self.image.get_rect()

        self.Events = IOEvent3()
        self.EventsHadDo = ElementHadDoEvent()
        self.visual = True
        self.zIndex = 0

    def update(self, *args):
        pass
