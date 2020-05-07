import math
import random

import pygame

from source.core.const.Const import gl_Font
from source.core.assembly.Painter import Painter
from source.core.math.MathConst import PI_DOUBLE
from source.core.math.MathUtil import mapping
from source.core.math.Vector import vec2, point2
from source.core.math.Noise import noise
from source.core.math.Shape import Circle
from source.view.baseClazz.Scene import Scene
from source.view.element.Elements import TextElement


class Particle:
    def __init__(self, width, height):
        self.w, self.h = width, height
        self.pos = vec2(random.randint(0, width), random.randint(0, height))
        self.vel, self.acc, self.prevPos = vec2(), vec2(), vec2()
        self.maxSpeed = 2

    def update(self):
        self.prevPos = self.pos
        self.vel += self.acc
        self.vel.limit(self.maxSpeed)
        self.pos += self.vel
        self.acc = self.acc.mul(0)

    def follow(self, scl, cols, vectors):
        x = math.floor(self.pos.x / scl)
        y = math.floor(self.pos.y / scl)
        index = x + y * cols
        try:
            force = vectors[index]
            self.applyForce(force)
        except IndexError:
            pass

    def applyForce(self, force):
        self.acc += force

    def show(self, surface):
        # Painter(surface).Pixel(self.pos, (255, 255, 255))
        Painter(surface, True).Circle(Circle(self.pos, 1), (0, 0, 0, 50), 0)
        self.edgesPrev()
        # pygame.draw.circle(surface, (255, 255, 255, 100), (int(self.pos.x), int(self.pos.y)), 2, 0)

    def edgesPrev(self):
        self.prevPos.x = self.pos.x
        self.prevPos.y = self.pos.y

    def edges(self):
        if self.pos.x > self.w:
            self.pos.x = 0
            self.edgesPrev()
        if self.pos.x < 0:
            self.pos.x = self.w
            self.edgesPrev()
        if self.pos.y > self.h:
            self.pos.y = 0
            self.edgesPrev()
        if self.pos.y < 0:
            self.pos.y = self.h
            self.edgesPrev()


class noiseTestScene(Scene):
    def __init__(self, *args):
        super(noiseTestScene, self).__init__(*args)
        self.caption = 'Perlin Noise'
        self.sceneCanvas = pygame.Surface((800, 600))
        self.sceneCanvas.fill((255, 255, 255))
        self.noiseScale = 0.02
        self._height, self._width = 600, 800
        self.inc = 0.1
        self.scl = 10
        self.zoff = 0
        self.cols, self.rows = math.floor(self._width / self.scl), math.floor(self._height / self.scl)
        self.particles = []
        self.flowField = [vec2()] * (self.cols * self.rows)
        for i in range(0, 2500):
            self.particles.append(Particle(self._width, self._height))

    # 噪音测试1
    def draw(self):
        for x in range(0, 800):
            noiseVal = noise((self.mouseX + x) * self.noiseScale, self.mouseY * self.noiseScale)
            Painter(self.screen).Lines([point2(x, self.mouseY + noiseVal * 80), point2(x, 600)],
                                       (noiseVal * 255, noiseVal * 255, noiseVal * 255), 1, 0)

    # def draw(self):
    #     yoff = 0
    #     for y in range(0, self.rows):
    #         xoff = 0
    #         for x in range(0, self.cols):
    #             index = x + y * self.cols
    #             angle = noise(xoff, yoff, self.zoff) * PI_DOUBLE * 4
    #             v = vec2.fromAngle(angle)
    #             v.setLen(1)
    #             self.flowField[index] = v
    #             xoff += self.inc
    #             # line = Line(point2(x * self.scl, y * self.scl), v.orient(), 10)
    #             # Painter(self.sceneCanvas).Line(line, (255, 255, 255), 1, 1)
    #
    #         yoff += self.inc
    #         self.zoff += 0.0003
    #
    #     for p in self.particles:
    #         p.follow(self.scl, self.cols, self.flowField)
    #         p.update()
    #         p.edges()
    #         p.show(self.sceneCanvas)
    #
    #     self.screen.blit(self.sceneCanvas, (0, 0))


class noise1DScene(Scene):
    def __init__(self, *args):
        super(noise1DScene, self).__init__(*args)

        self.pixies = list()

    def setup(self):
        for i in range(0, self.width, 20):
            y = mapping(noise(10), 0, 1, 0, 600)
            self.pixies.append(point2(i - 1, y))
            self.pixies.append(point2(i, 300))
            # self.pixies.append(point2(i + 1, y))

    def draw(self):
        self.Lines(self.pixies, (255, 255, 255), 1, 0, 1)
        # for p in self.pixies:
        #     self.Pixel(p, (255, 255, 255))
