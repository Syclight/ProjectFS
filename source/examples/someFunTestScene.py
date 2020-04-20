import math
import random
from math import cos, sin

from source.controller.assembly.Painter import Painter
from source.core.math.Vector import point2
from source.core.math.MathConst import PI, PI_DOUBLE
from source.core.math.MathUtil import mapping
from source.core.math.Shape import Circle, Line
from source.view.baseClazz.Scene import Scene


class drawingBoard(Scene):
    """画板

    展示了Scene一些内置对象与变量的基本用法
    """

    def __init__(self, *args):
        super(drawingBoard, self).__init__(*args)
        self.color = (255, 255, 255)
        self.stork = 1
        self.isFill = False
        self.__start = point2()
        self.interval = 10

    def draw(self):
        if not self.__start.isZero():
            Painter(self.screen).Lines([self.__start, point2(self.mousePos)], self.color, self.stork, 0, 1)
            self.__start = point2(self.mousePos)

    def doMouseButtonDownEvent(self, Button):
        if Button == 1:
            self.__start = point2(self.mousePos)

    def doMouseButtonUpEvent(self, Button):
        if Button == 1:
            self.__start = point2()


class createWave(Scene):
    """创建波纹

    这个例子展示了Scene内置对象 sceneCanvas 与 screen的关系。

    试着将isFill设置为True或删去，或将sceneCanvas相关的方法移动到初始化方法里，看看结果。
    """

    def __init__(self, *args):
        super(createWave, self).__init__(*args)
        self.isFill = False
        self.t = 0.0

    def draw(self):
        self.sceneCanvas.fill((0, 0, 0))
        self.sceneCanvas.set_alpha(20)
        # 创建圆
        for i in range(0, 800, 30):
            for j in range(0, 600, 30):
                # 每个圆的初始位置取决于鼠标位置
                ax = mapping(self.mouseX, 0, 800, -4 * PI, 4 * PI)
                ay = mapping(self.mouseY, 0, 600, -4 * PI, 4 * PI)

                # 根据圆的位置获取角度
                angle = ax * (i / 800) + ay * (j / 600)

                # 每个圆做圆周运动
                x = i + 20 * cos(2 * PI * self.t + angle)
                y = j + 20 * sin(2 * PI * self.t + angle)

                Painter(self.sceneCanvas).Circle(Circle(x, y, 10), (0, 255, 0), 0)
        self.t += 0.01  # 更新时间
        self.screen.blit(self.sceneCanvas, (0, 0))


class sketchSphere(Scene):
    """在2维平面上画一个球

    这个例子展示了Scene内置对象 sceneCanvas 与 screen的关系。

    或将sceneCanvas相关的方法移动到draw方法里，看看结果。
    """

    def __init__(self, *args):
        super(sketchSphere, self).__init__(*args)
        self.t = 0.0
        self.sceneCanvas.fill((255, 255, 255))
        self.sceneCanvas.set_alpha(150)

    def __randomChord(self):
        angle1 = random.uniform(0, PI_DOUBLE)
        x_pos1, y_pos1 = self.width / 2 + 200 * cos(angle1), self.height / 2 + 200 * sin(angle1)
        angle2 = random.uniform(0, PI_DOUBLE)
        x_pos2, y_pos2 = self.width / 2 + 200 * cos(angle2), self.height / 2 + 200 * sin(angle2)

        Painter(self.sceneCanvas).Lines([point2(x_pos1, y_pos1), point2(x_pos2, y_pos2)], (0, 0, 0), 1, 0, 1)
        self.screen.blit(self.sceneCanvas, (0, 0))

    def draw(self):
        self.__randomChord()
        self.__randomChord()


class chain(Scene):
    """来源于p5.js，基于 Keith Peters 的代码

    随鼠标移动的一条分段式线条。

    每段之间的相对角度是用 atan2() 计算的，位置是用 sin() 和 cos() 计算的。
    """

    def __init__(self, *args):
        super(chain, self).__init__(*args)
        self.segNum = 20
        self.segLength = 30
        self.x, self.y = [0] * self.segNum, [0] * self.segNum

    def __dragSegment(self, i, xin, yin):
        dx, dy = xin - self.x[i], yin - self.y[i]
        angle = math.atan2(dy, dx)
        self.x[i], self.y[i] = xin - cos(angle) * self.segLength, yin - sin(angle) * self.segLength
        self.__segment(self.x[i], self.y[i], angle)

    def __segment(self, x, y, a):
        line = Line(point2(x, y), a, self.segLength)
        Painter(self.screen).Line(line, (255, 255, 255), 10, 1)

    def draw(self):
        self.__dragSegment(0, self.mouseX, self.mouseY)
        for i in range(0, len(self.x) - 1):
            self.__dragSegment(i + 1, self.x[i], self.y[i])
