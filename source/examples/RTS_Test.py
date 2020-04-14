import math

import pygame

from source.const.Const import gl_Font_opt, gl_Font
from source.controller.assembly.A_star import AStartArea
from source.controller.assembly.Shape import Rectangle
from source.util.Math2d import point2
from source.view.baseClazz.Actor import Actor
from source.view.baseClazz.Scene import Scene
from source.view.element.Elements import TextElement


class RobotActor(Actor):
    def __init__(self, area):
        path = 'F:/练习/PyCharm/PygameTest/resource/Test/robot.png'
        super(RobotActor, self).__init__(pygame.image.load(path), area)

    def draw(self, screen):
        screen.blit(self.texture, (self.area.left(), self.area.top()))

    def run(self, point, speed):
        pos = self.area.barycenter()
        if pos.x == point.x and pos.y == point.y:
            return True
        else:
            dir_x = -1 if pos.x > point.x else 1
            dir_y = -1 if pos.y > point.y else 1
            pos.x += dir_x * speed
            pos.y += dir_y * speed
            self.area.rebuildForBarycenter(pos)
            return False

    def setLocal(self, local):
        self.area = local


class Container(Actor):
    def __init__(self, area):
        path = 'F:/练习/PyCharm/PygameTest/resource/Test/container.jpg'
        super(Container, self).__init__(pygame.image.load(path), area)

    def draw(self, screen):
        screen.blit(self.texture, (self.area.top(), self.area.left()))


class RobotRunScene(Scene):
    def __init__(self, screen, config, startClock):
        super(RobotRunScene, self).__init__(screen, config, startClock)
        self.__A_Robot = RobotActor(Rectangle(0, 0, 100, 100))
        self.__As_MAP = AStartArea(Rectangle(0, 0, 800, 600), 8, 6)
        self.__A_Container1 = Container(Rectangle(0, 0, 100, 100))
        self.__E_Msg = TextElement(pygame.Rect(600, 0, 200, 60), 'Robotlocal:(0, 0)\nMouselocal:(0, 0)', gl_Font,
                                   12, (255, 255, 255), 1)
        self.__E_Msg2 = TextElement(pygame.Rect(600, 40, 200, 600), 'Astart:\n', gl_Font, 12, (255, 255, 255), 1)
        self.__pathList = []
        self.__normalLis = []
        self.__build_As_Map()
        self.__isNextRun = True
        self.__i = 0
        self.__nowP = (0, 0)
        self.__end = (0, 0)

    def __build_As_Map(self):
        self.__As_MAP.setStart((0, 0))

    def __updateMap(self, point):
        x = int(self.__A_Robot.area.x / 100)
        y = int(self.__A_Robot.area.y / 100)
        self.__As_MAP.setStart((x, y))
        x = int(point[0] / 100)
        y = int(point[1] / 100)
        self.__As_MAP.setEnd((x, y))

    def __normalList(self):
        self.__normalLis.clear()
        h, w = self.__As_MAP.unit_h, self.__As_MAP.unit_w
        bc = self.__A_Robot.area.barycenter()
        for p in self.__pathList:
            self.__normalLis.append(point2(p[0] * h, p[1] * w))
        self.__normalLis[0] = point2(bc.x, bc.y)
        self.__normalLis[-1] = point2(self.__end[0], self.__end[1])

    def draw(self):
        length = len(self.__normalLis)
        if self.__i < length:
            if self.__A_Robot.run(self.__normalLis[self.__i], 10):
                self.__i += 1
        self.__A_Robot.draw(self.screen)
        self.__E_Msg.draw(self.screen)
        self.__E_Msg2.draw(self.screen)

    def doClockEvent(self, NowClock):
        p = self.__A_Robot.area.barycenter()
        p2 = self.__end
        lis_str = 'A-start:\n'
        for _p in self.__normalLis:
            lis_str += str(_p) + '\n'
        self.__E_Msg.setText('Robotlocal:({}, {})\nMouselocal:({}, {})'.format(p.x, p.y, p2[0], p2[1]))
        self.__E_Msg2.setText(lis_str)

    def doMouseButtonDownEvent(self, MousePos, Button):
        if Button == 1:
            self.__end = MousePos
            self.__updateMap(self.__end)
            self.__pathList = self.__As_MAP.run()
            self.__normalList()
            self.__As_MAP.refresh()
            self.__i = 0
