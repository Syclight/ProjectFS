import math
import random
from math import cos, sin

import pygame

from source.core.assembly.Painter import Painter
from source.core.math.Vector import point2, vec2
from source.core.math.MathConst import PI, PI_DOUBLE
from source.core.math.MathUtil import mapping
from source.core.math.Shape import Circle, Line
from source.core.multimedia.MusicPlayer import musicPlayer
from source.view.baseClazz.Scene import Scene


class drawingBoard(Scene):
    """画板 按q清屏

    展示了Scene一些内置对象与变量的基本用法
    """

    def __init__(self, *args):
        super(drawingBoard, self).__init__(*args)
        self.color = (255, 255, 255)
        self.stork = 1
        self.isFill = False
        self.__start = point2()
        self.interval = 10
        self.caption = '测试场景：画板  按鼠标左键进行绘制，q键清屏'

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

    def doKeyEvent(self, Key, Mod, Type, Unicode=None):
        if Key == 113:
            self.screen.fill((0, 0, 0))


class createWave(Scene):
    """创建波纹

    这个例子展示了Scene内置对象 sceneCanvas 与 screen的关系。

    试着将isFill设置为True或删去，或将sceneCanvas相关的方法移动到初始化方法里，看看结果。
    """

    def __init__(self, *args):
        super(createWave, self).__init__(*args)
        self.isFill = False
        self.t = 0.0
        self.sceneCanvas = self.screen.copy()
        self.caption = '测试场景：波纹'

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
    """在2维平面上画一个球体

    这个例子展示了Scene内置对象 sceneCanvas 与 screen的关系。

    或将sceneCanvas相关的方法移动到draw方法里，看看结果。
    """

    def __init__(self, *args):
        super(sketchSphere, self).__init__(*args)
        self.t = 0.0
        self.sceneCanvas = self.screen.copy()
        self.sceneCanvas.fill((255, 255, 255))
        self.sceneCanvas.set_alpha(150)
        self.caption = '测试场景：草稿'

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
    """改写自p5.js范例，基于 Keith Peters 的代码

    随鼠标移动的一条分段式线条。

    每段之间的相对角度是用 atan2() 计算的，位置是用 sin() 和 cos() 计算的。
    """

    def __init__(self, *args):
        super(chain, self).__init__(*args)
        self.segNum = 10
        self.segLength = 40
        self.x, self.y = [0] * self.segNum, [0] * self.segNum
        self.caption = '测试场景：链条'

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


class paramEquation(Scene):
    """这个是参数方程的例子， 改写自p5.js范例，灵感来源于Alexander Miller的视频"""

    def __init__(self, *args):
        super(paramEquation, self).__init__(*args)
        self.t = 0  # x 和 y 所依靠的参数通常被视为 t
        self.caption = '数学之美：参数方程'

    def draw(self):
        for i in range(0, 100):
            s_point = point2(self.width / 2 + self.__x1(i), self.height / 2 + self.__y1(i))
            e_point = point2(self.width / 2 + self.__x2(i) + 20, self.height / 2 + self.__y2(i) + 20)
            Painter(self.screen).Lines([s_point, e_point], (255, 255, 255), 1, 0, 1)
        self.t += 0.15

    # 改变直线的初始 x 坐标
    def __x1(self, i):
        return sin((self.t + i) / 10) * 125 + sin((self.t + i) / 20) * 125 + sin((self.t + i) / 30) * 125

    # 改变直线的初始 y 坐标
    def __y1(self, i):
        return cos((self.t + i) / 10) * 125 + cos((self.t + i) / 20) * 125 + cos((self.t + i) / 30) * 125

    # 改变直线的最终 x 坐标
    def __x2(self, i):
        return sin((self.t + i) / 15) * 125 + sin((self.t + i) / 25) * 125 + sin((self.t + i) / 35) * 125

    # 改变直线的最终 y 坐标
    def __y2(self, i):
        return cos((self.t + i) / 15) * 125 + cos((self.t + i) / 25) * 125 + cos((self.t + i) / 35) * 125


class kaleidoscope(Scene):
    """一个很有趣的万华筒，改写自p5.js的范例 按q键清空屏幕

    万花筒是一个光学仪器，具有两个或多个互相倾斜的反射面。 此范例尝试模仿万花筒的效果。 通过 symmetry 变量设定反射的数量，并开始在屏幕上绘制
    """

    def __init__(self, *args):
        super(kaleidoscope, self).__init__(*args)
        self.symmetry = 6
        self.angle = math.radians(360 / self.symmetry)
        self.isFill = False
        self.v = vec2(self.width / 2, self.height / 2)
        self.caption = '测试场景：万花筒  按下鼠标按键进行绘制，按q键清屏'
        self.painter = Painter(self.screen)

    def draw(self):
        if 0 < self.mouseX < self.width and 0 < self.mouseY < self.height:
            mx = self.mouseX - self.width / 2
            my = self.mouseY - self.height / 2
            pmx = self.lastMousePos[0] - self.width / 2
            pmy = self.lastMousePos[1] - self.height / 2

            v1_n = vec2(self.width / 2 + mx, self.height / 2 + my)
            v1_l = vec2(self.width / 2 + pmx, self.height / 2 + pmy)
            v2_n = vec2(self.width / 2 + mx, self.height / 2 - my)
            v2_l = vec2(self.width / 2 + pmx, self.height / 2 - pmy)

            if self.mousePressed:
                self.painter.push()
                for i in range(0, self.symmetry):
                    # v1_n = self.__rotateBy(v1_n, self.width / 2, self.height / 2)
                    # v1_l = self.__rotateBy(v1_l, self.width / 2, self.height / 2)
                    # v2_n = self.__rotateBy(v2_n, self.width / 2, self.height / 2)
                    # v2_l = self.__rotateBy(v2_l, self.width / 2, self.height / 2)

                    self.painter.rotate(self.width / 2, self.height / 2, self.angle)
                    self.painter.Lines([v1_n, v1_l], (255, 255, 255), 1, 0, 1)
                    self.painter.Lines([v2_n, v2_l], (255, 255, 255), 1, 0, 1)
                self.painter.pop()

    # 将v以(x, y)点为中心进行旋转
    # def __rotateBy(self, v, x, y):
    #     v = vec2(v.x - x, v.y - y)
    #     v = v.rotate(self.angle)
    #     v = vec2(v.x + x, v.y + y)
    #     return v

    def doKeyEvent(self, Key, Mod, Type, Unicode=None):
        if Key == 113:
            self.screen.fill((0, 0, 0))


class snowScene(Scene):
    """下雪的场景, 雪会随着音乐变化"""

    def __init__(self, *args):
        super(snowScene, self).__init__(*args)
        self.snowflakes = []
        self.music_path = 'resource/Test/雪之华.wav'
        # self.music_path = 'E:/Music/星之所在.wav'
        self.caption = '测试场景：音乐与动画交互  雪之华-中岛美嘉'
        self.player = musicPlayer()
        self.player.add('0', self.music_path)
        pygame.mixer.music.load(self.music_path)

    def draw(self):
        if not pygame.mixer.music.get_busy():
            self.player.active('0')
            pygame.mixer.music.play()
        ma, fps = 0, 60
        if self.FPS != 0:
            fps = self.FPS
        lis = self.player.getMsg('0', round(1 / fps * 8000))
        for n in lis:
            if n > ma:
                ma = n

        if ma != 0:
            p = mapping(ma, 0, 6000, 0, 5)
            p = round(p)
        else:
            p = 0

        t = self.frameCount / 180

        for i in range(random.randint(0, p)):
            self.snowflakes.append(snowFlake(self.width, self.height))

        for flake in self.snowflakes:
            flake.update(t, self.snowflakes)
            flake.display(self.screen)


class snowFlake:
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.posX = 0
        self.posY = random.randint(-50, 0)
        self.initial_angle = random.uniform(0, PI_DOUBLE)
        self.size = random.randint(2, 5)

        self.radius = math.sqrt(random.uniform(0, pow(self.width / 2, 2)))

    def update(self, time, ary):
        w = 0.6  # 角速度
        angle = w * time + self.initial_angle

        self.posX = self.width / 2 + self.radius * math.sin(angle)
        self.posY += pow(self.size, 0.5)

        if self.posY > self.height:
            ary.remove(self)

    def display(self, sur):
        Painter(sur).Circle((self.posX, self.posY, self.size / 2), (255, 255, 255), 1)


class MandelbrotSet(Scene):
    """分形（fractal）模拟： 曼德勃罗集 Mandelbrot set"""

    def __init__(self, *args):
        super(MandelbrotSet, self).__init__(*args)
        self.caption = '测试场景: MandelbrotSet'

        self.width, self.height = 600, 600
        self.canvas = pygame.Surface((self.width, self.height))

        self.max_iteration = 100
        for x in range(self.width):
            for y in range(self.height):
                a = mapping(x, 0, self.width, -1.5, 1.5)
                b = mapping(y, 0, self.height, -1.5, 1.5)
                ca, cb = a, b

                n = 0
                while n < self.max_iteration:  # 迭代
                    aa, bb = a * a - b * b, 2 * a * b
                    a, b = aa + ca, bb + cb
                    if abs(a + b) > 16:
                        break
                    n += 1

                bright = mapping(n, 0, self.max_iteration, 0, 1)
                bright = mapping(math.sqrt(bright), 0, 1, 0, 255)
                if n is self.max_iteration:
                    bright = 0

                self.canvas.set_at([x, y], (bright, bright, bright))

    def draw(self):
        self.screen.blit(self.canvas, self.canvas.get_rect())


class JuliaSet(Scene):
    """分形（fractal）模拟： 茱莉亚集 JuliaSet set"""

    def __init__(self, *args):
        super(JuliaSet, self).__init__(*args)
        self.caption = '测试场景: JuliaSet'

        self.real = 0.285  # -0.70176  # -0.8 # 实部
        self.imaginary = 0.01  # -0.3842  # 0.156 # 虚部

        self.width, self.height = 600, 600
        self.canvas = pygame.Surface((self.width, self.height))

        self.w = 5
        self.h = (self.w * self.height) / self.width

        self.x_min = - self.w / 2
        self.y_min = - self.h / 2
        self.x_max = self.x_min + self.w
        self.y_max = self.y_min + self.h

        self.dx = (self.x_max - self.x_min) / self.width
        self.dy = (self.y_max - self.y_min) / self.height

        self.max_iteration = 100

        self.y = self.y_min
        for i in range(self.width):
            self.x = self.x_min
            for j in range(self.height):
                a = self.y
                b = self.x

                n = 0
                while n < self.max_iteration:  # 迭代
                    aa, bb = a * a, b * b
                    ab_double = 2 * a * b
                    a, b = aa - bb + self.real, ab_double + self.imaginary
                    if aa * aa + bb * bb > 16:
                        break
                    n += 1

                if n == self.max_iteration:
                    self.canvas.set_at([i, j], (0, 0, 0))
                else:
                    norm = mapping(n, 0, self.max_iteration, 0, 1)
                    norm = mapping(math.sqrt(norm), 0, 1, 0, 255)
                    self.canvas.set_at([i, j], (norm, norm, norm))

                self.x += self.dx
            self.y += self.dy

    def draw(self):
        self.screen.blit(self.canvas, self.canvas.get_rect())


class IFS(Scene):
    """分形（fractal）模拟： Iterated function system 迭代分形系统"""

    def __init__(self, *args):
        super(IFS, self).__init__(*args)
        self.caption = '测试场景: Iterated function system 迭代分形系统'

        self.width, self.height = 600, 600
        self.canvas = pygame.Surface((self.width, self.height))

        self.max_iteration = 100
        for x in range(self.width):
            for y in range(self.height):
                a = mapping(x, 0, self.width, -1.5, 1.5)
                b = mapping(y, 0, self.height, -1.5, 1.5)
                ca, cb = a, b

                n = 0
                while n < self.max_iteration:  # 迭代
                    ran = random.randint(0, 3)
                    if ran == 0:
                        a, b = self.__rul_0(a, b, ca, cb)
                    elif ran == 1:
                        a, b = self.__rul_1(a, b, ca, cb)
                    elif ran == 2:
                        a, b = self.__rul_2(a, b, ca, cb)
                    elif ran == 3:
                        a, b = self.__rul_3(a, b, ca, cb)
                    # aa, bb = a * a - b * b, 2 * a * b
                    # a, b = aa + ca, bb + cb
                    if abs(a + b) > 16:
                        break
                    n += 1

                bright = mapping(n, 0, self.max_iteration, 0, 1)
                bright = mapping(math.sqrt(bright), 0, 1, 0, 255)
                if n is self.max_iteration:
                    bright = 0

                self.canvas.set_at([x, y], (bright, bright, bright))

    @staticmethod
    def __rul_0(a, b, ca, cb):
        aa, bb = a * a - b * b, 2 * a * b
        return aa + ca, bb + cb

    @staticmethod
    def __rul_1(a, b, ca, cb):
        aa, bb = a * a + b * b, 2 * a * b
        return aa + ca, bb + cb

    @staticmethod
    def __rul_2(a, b, ca, cb):
        aa, bb = a * a, 2 * a * b
        return aa + ca, bb + cb

    @staticmethod
    def __rul_3(a, b, ca, cb):
        aa, bb = b * b, 2 * a * b
        return aa + ca, bb + cb

    def draw(self):
        self.screen.blit(self.canvas, self.canvas.get_rect())


class LSystemScene(Scene):
    """L-System 分形树，灵感来源于the Coding Train的视频"""

    def __init__(self, *args):
        super(LSystemScene, self).__init__(*args)

        rule_str1_1 = 'F->FF+[+F-F-F]-[-F+F+F]'
        rule_str1_2 = 'X->[-FX]+FX'
        rule_str1_3 = 'F->F[+FF][-FF]F[-F][+F]F'

        # rule_str2_1 = 'X->F+[[X]-X]-F[-FX]+X'
        rule_str2_1 = 'X->F[+X]F[-X]+X'
        rule_str2_2 = 'F->FF'

        self.__rule = self.rule(rule_str1_1)
        self.__rule2_1 = self.rule(rule_str2_1)
        self.__rule2_2 = self.rule(rule_str2_2)

        self.isFill = False
        self.caption = 'L-Systems生成树，鼠标点击，观看树的生长'

        self.l_system = LSystem([self.__rule], 'F', math.radians(35), self.screen)
        self.l_system.len = 10

    class rule:  # 内部类
        def __init__(self, _str):
            self.__str = _str
            self.a, self.b = _str.split('->')

        def __str__(self):
            return self.__str

    def setup(self):
        self.createTextElement('规则：' + str(self.__rule), color=(153, 217, 234))
        self.createTextElement('根:' + 'F', color=(153, 217, 234))
        pass

    def doMouseButtonDownEvent(self, Button):
        self.l_system.generate(self.width / 2, self.height)
        # self.createTextElement(self.l_system.getSentence())


class LSystem:
    def __init__(self, rules, axiom, angle, sur):
        self.__axiom = axiom
        self.__rules = rules
        self.__sentence = self.__axiom
        self.__angle = angle
        self.len = 10
        self.painter = Painter(sur)

    def generate(self, x, y):
        nextSentence = ''
        for i in range(len(self.__sentence)):
            current = self.__sentence[i]
            found = False
            for j in range(len(self.__rules)):
                if current == self.__rules[j].a:
                    found = True
                    nextSentence += self.__rules[j].b
            if not found:
                nextSentence += current

        self.__sentence = nextSentence
        self.__show(x, y)

    def getSentence(self):
        return self.__sentence

    def __show(self, x=0, y=0):
        self.painter.resetCurrentMat()
        self.painter.translate(x, y)
        for i in range(len(self.__sentence)):
            current = self.__sentence[i]
            if current == 'F':
                self.painter.Lines([point2(0, 0), point2(0, -self.len)], (255, 255, 255), 1, 0)
                self.painter.translate(0, -self.len)
            elif current == '+':
                self.painter.rotate(self.__angle)
            elif current == '-':
                self.painter.rotate(-self.__angle)
            elif current == '[':
                self.painter.push()
            elif current == ']':
                self.painter.pop()


