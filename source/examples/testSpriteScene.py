import random

import pygame

from source.const.Const import gl_WindowHeight
from source.controller.dataStructure.QuadTree import RectangleRange
from source.view.scene.Scenes import Scene
from source.view.baseClazz.Sprite import Sprite, SpriteGroup
from source.controller.assembly.Shape import Rectangle


class GameSprite(Sprite):
    def __init__(self, image, speed=1):
        super().__init__(image)
        self.speed = speed

    def update(self, *args):
        self.rect.x += self.speed
        self.rect.y += self.speed
        if self.rect.y > gl_WindowHeight or self.rect.y < 0:
            self.speed = -self.speed


class gearSprite(Sprite):
    def __init__(self, image, rect):
        super().__init__(image, rect)
        self._image = self.image
        self.rotate = 0

    def update(self, *args):
        self.rotate += 1
        self.image = pygame.transform.rotate(self._image, self.rotate)
        self.rect = self.image.get_rect(center=self.rect.center)


class CubeSprite(Sprite):
    def __init__(self, image, rect):
        super(CubeSprite, self).__init__(image, rect)
        self.__x = self.rect.x
        self.__y = self.rect.y
        self.image.set_alpha(100)
        self.highLight = False

    def update(self, *args):
        self.highLight = False
        self.rect = pygame.Rect(self.__x + random.uniform(-1, 1), self.__y + random.uniform(-1, 1), self.rect.w,
                                self.rect.h)
        self.collidedArea = Rectangle(self.rect.x, self.rect.y, self.rect.w, self.rect.h)

    def draw(self, surface):
        if self.highLight:
            self.image.set_alpha(255)
        else:
            self.image.set_alpha(100)
        surface.blit(self.image, self.rect)


def chPos(step, sprite, isY):
    if isY:
        sprite.setRect(pygame.Rect(sprite.rect.x, sprite.rect.y + step, sprite.rect.w, sprite.rect.h))
    else:
        sprite.setRect(pygame.Rect(sprite.rect.x + step, sprite.rect.y, sprite.rect.w, sprite.rect.h))


# test 播放动画
# class testSpriteScene(Scene):
#     def __init__(self, screen, framework-config):
#         super(testSpriteScene, self).__init__(screen, framework-config)
#         self.img = pygame.image.load('F:/练习/PyCharm/PygameTest/resource/Img/TEST_ANIM.jpg').convert_alpha()
#         self.enemy = GameSprite(clipResImg(self.img, pygame.Rect(0, 0, 278, 153), (45, 45, 45)), 0)
#         self.enemy.rect.x = 200
#         self.enemy.rect.y = 200
#         # self.enemy1 = GameSprite(pygame.image.load("F:/练习/PyCharm/PygameTest/resource/Img/gear.png"), 2)
#         self.enemy1 = gearSprite(pygame.image.load("F:/练习/PyCharm/PygameTest/resource/Img/gear.png").convert_alpha(),
#                                  pygame.Rect(220, 220, 548, 549))
#         # 创建精灵组
#         self.enemy_group = SpriteGroup(RectangleRange(0, 0, 800, 600), self.enemy, self.enemy1)
#         #self.enemy_group = pygame.sprite.Group(self.enemy, self.enemy1)
#         self.enemy.Events.appendEvent(ioEvent3Enum.key_W | ioEvent3Enum.keyDowning,
#                                       lambda: chPos(-1, self.enemy, True), 1)
#         self.enemy.Events.appendEvent(ioEvent3Enum.key_S | ioEvent3Enum.keyDowning,
#                                       lambda: chPos(1, self.enemy, True), 1)
#         self.enemy.Events.appendEvent(ioEvent3Enum.key_A | ioEvent3Enum.keyDowning,
#                                       lambda: chPos(-1, self.enemy, False), 1)
#         self.enemy.Events.appendEvent(ioEvent3Enum.key_D | ioEvent3Enum.keyDowning,
#                                       lambda: chPos(1, self.enemy, False), 1)
#         self.interval = None
#         self.clipRect = pygame.Rect(0, 0, 278, 153)
#         self.__flag_raw = 1
#
#     def draw(self):
#         self.enemy_group.update()
#         self.enemy_group.draw(self.screen)
#
#     def doClockEvent(self, nowClock):
#         print(self.enemy_group.getCollideDict())
#
#         self.interval = nowClock - self.startClock
#         if self.interval >= 100:
#             self.startClock = nowClock
#             if self.clipRect.top >= 612 and self.clipRect.left >= 278:
#                 self.clipRect = pygame.Rect(-278, 0, 278, 153)
#                 self.__flag_raw = 1
#             if self.__flag_raw == 1:
#                 self.clipRect = pygame.Rect(self.clipRect.left + self.clipRect.width, self.clipRect.top,
#                                             278, 153)
#                 self.__flag_raw = 2
#             elif self.__flag_raw == 2:
#                 self.clipRect = pygame.Rect(0, self.clipRect.top + self.clipRect.height, 278, 153)
#                 self.__flag_raw = 1
#             self.enemy.image = clipResImg(self.img, self.clipRect, (45, 45, 45))
#
#     def doKeyPressedEvent(self, keyPressedList):
#         for key in keyPressedList:
#             self.enemy.Events.doKeyboardKeyDowning(exKey(key))
#             self.enemy1.Events.doKeyboardKeyDowning(exKey(key))


# test 组内碰撞检测
class testSpriteScene(Scene):
    def __init__(self, screen, config):
        super(testSpriteScene, self).__init__(screen, config)
        self.img = pygame.Surface((5, 5)).convert()
        self.img.fill((255, 255, 255))
        self.sprintsGroup1 = SpriteGroup(RectangleRange(0, 0, 800, 600))
        for i in range(0, 1000):
            x, y = random.randint(0, 800), random.randint(0, 600)
            self.sprintsGroup1.add(CubeSprite(self.img, pygame.Rect(x, y, 5, 5)))

    def draw(self):
        _dict = self.sprintsGroup1.getCollideDict()
        for w in _dict.keys():
            w.highLight = True
        self.sprintsGroup1.draw(self.screen)
        self.sprintsGroup1.update()

    def doClockEvent(self, NowClock):
        pass

    # def doKeyPressedEvent(self, keyPressedList):
    #     for key in keyPressedList:
    #         self.sp1.Events.doKeyboardKeyDowning(exKey(key))
