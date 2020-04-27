import random

import pygame

from source.const.Const import gl_Font
from source.core.assembly.A_star import AStarArea, CoordinateException
from source.core.math.Vector import point2
from source.core.math.Shape import Rectangle
from source.core.assembly.Painter import Painter
from source.view.baseClazz.Actor import Actor
from source.view.baseClazz.Scene import Scene
from source.view.element.Elements import TextElement


class RobotActor(Actor):
    def __init__(self, area):
        path = 'F:/练习/PyCharm/PygameTest/resource/Test/robot.png'
        super(RobotActor, self).__init__(pygame.image.load(path), area)
        self.__linePoints = [point2(), point2()]
        self.__startCord = self.area.barycenter()
        self.max_speed = 10
        self.__pathList = []
        self.__interPath = []

    def setPathList(self, lis):
        self.__pathList = lis.copy()

    def draw(self, screen):
        screen.blit(self.texture, (self.area.left(), self.area.top()))
        sp, ep = self.__linePoints[0], self.__linePoints[1]
        if not sp.same(ep):
            Painter(screen).Lines(self.__linePoints, (0, 255, 0), 1, 0)

    def update(self, point, speed, end_point):
        pos = self.area.barycenter()
        if point.same(end_point):
            pos.x = point.x
            pos.y = point.y
            self.__linePoints.clear()
            self.__linePoints = [end_point, pos]
            self.area.rebuildForBarycenter(pos)
        if pos.same(point):
            return True
        else:
            dir_x, dir_y = 0, 0
            if pos.x < point.x:
                dir_x = 1
            elif pos.x > point.x:
                dir_x = -1

            if pos.y < point.y:
                dir_y = 1
            elif pos.y > point.y:
                dir_y = -1

            pos.x += dir_x * speed
            pos.y += dir_y * speed

        self.__linePoints.clear()
        self.__linePoints = [end_point, pos]
        self.area.rebuildForBarycenter(pos)
        return False

    def getLocal(self):
        return self.area.barycenter()


class Container(Actor):
    def __init__(self, area):
        path = 'F:/练习/PyCharm/PygameTest/resource/Test/container.jpg'
        super(Container, self).__init__(pygame.image.load(path), area)

    def draw(self, screen):
        screen.blit(self.texture, (self.area.left(), self.area.top()))


class RobotRunScene(Scene):
    def __init__(self, screen, config, startClock):
        super(RobotRunScene, self).__init__(screen, config, startClock)
        self.w, self.h = self.screen.get_width(), self.screen.get_height()
        self.__As_MAP = AStarArea(Rectangle(0, 0, 800, 600), 80, 60)
        self.__containers = []
        for i in range(0, 6):
            x = int(random.randint(100, self.w - 150) / 10) * 10
            y = int(random.randint(100, self.h - 150) / 10) * 10
            w = int(random.randint(50, 150) / 10) * 10
            h = int(random.randint(50, 150) / 10) * 10
            self.__containers.append(Container(Rectangle(x, y, w, h)))
            _x, _y = int(x / self.__As_MAP.unit_w), int(y / self.__As_MAP.unit_h)
            _w, _h = int(w / self.__As_MAP.unit_w), int(h / self.__As_MAP.unit_h)
            self.__As_MAP.addObstacleArea(_x, _w, _y, _h)

        self.__A_Robot = RobotActor(Rectangle(0, 0, 100, 100))
        self.__E_Msg = TextElement(pygame.Rect(600, 0, 200, 60), 'Robotlocal:(0, 0)\nMouselocal:(0, 0)', gl_Font,
                                   12, (255, 255, 255), 1)
        self.__E_Msg2 = TextElement(pygame.Rect(600, 40, 200, 600), 'Astart:\n', gl_Font, 10, (255, 255, 255), 1)
        self.__pathList = []
        self.__normalLis = []
        self.__build_As_Map()
        self.__i = 0
        self.__end = (0, 0)

    def __build_As_Map(self):
        self.__As_MAP.setStart((0, 0))

    def __updateMap(self, point):
        h, w = self.__As_MAP.unit_h, self.__As_MAP.unit_w
        pos = self.__A_Robot.getLocal()
        x = int(pos.x / w)
        y = int(pos.y / h)
        try:
            self.__As_MAP.setStart((x, y))
        except CoordinateException as e:
            return e.pos
        x = int(point[0] / w)
        y = int(point[1] / h)
        try:
            self.__As_MAP.setEnd((x, y))
        except CoordinateException as e:
            return e.pos

    def __normalList(self):
        self.__normalLis.clear()
        h, w = self.__As_MAP.unit_h, self.__As_MAP.unit_w
        for p in self.__pathList:
            self.__normalLis.append(point2(p[0] * w, p[1] * h))
        if len(self.__normalLis) > 1:
            self.__normalLis.pop(0)
        self.__A_Robot.setPathList(self.__normalLis)

    def draw(self):
        # for e in self.__As_MAP.getObstaclesList():
        #     Painter(self.screen).Rect(Rectangle(e[0] * 10, e[1] * 10, 10, 10), (255, 255, 255), 0)
        for container in self.__containers:
            container.draw(self.screen)
        self.__A_Robot.draw(self.screen)
        self.__E_Msg.draw(self.screen)
        self.__E_Msg2.draw(self.screen)

    def doClockEvent(self, NowClock):
        if self.__i < len(self.__normalLis):
            if self.__A_Robot.update(self.__normalLis[self.__i], 5, self.__normalLis[-1]):
                self.__i += 1
        p = self.__A_Robot.area.barycenter()
        p2 = self.__end
        lis_str = 'A-start:\n'
        for _p in self.__normalLis:
            lis_str += str(_p) + '\n'
        self.__E_Msg.setText('Robotlocal:({}, {})\nMouselocal:({}, {})\n'.format(p.x, p.y, p2[0], p2[1]))
        self.__E_Msg2.setText(lis_str)

    def doMouseButtonDownEvent(self, Button):
        if Button == 1:
            self.__end = self.mousePos
            pos = self.__updateMap(self.__end)
            if pos:
                return
            self.__pathList = self.__As_MAP.run()
            self.__normalList()
            self.__As_MAP.refresh()
            self.__i = 0
