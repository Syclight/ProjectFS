import math
import random
import pygame

from source.core.assembly.IOEvent import IOEvent3, ioEvent3Enum
from source.core.math.MathConst import PI_HALF
from source.core.math.Shape import Rectangle
from source.core.math.Vector import vec2, vec3
from source.core.math.MathUtil import constrain
from source.util.ToolsFuc import exKey
from source.view.baseClazz.Scene import Scene


class Mover:
    def __init__(self, location, constraintScope, mass=None):
        self.location = location
        self.velocity = vec2()
        self.acceleration = vec2()
        self.constraintScope = constraintScope
        self.mass = mass
        if self.mass is None:
            self.mass = random.randint(1, 10)

    def display(self, screen):
        loc = int(self.location.x), int(self.location.y)
        pygame.draw.circle(screen, (0, 255, 0), loc, self.mass * 2 + 14, 1)

    def applyForce(self, force):
        f = force.mul(1 / self.mass)
        self.acceleration += f

    def update(self):
        self.velocity += self.acceleration
        self.location += self.velocity
        self.acceleration = self.acceleration.mul(0)

    def edges(self):
        right = self.constraintScope.right()
        bottom = self.constraintScope.bottom()
        left = self.constraintScope.left()
        top = self.constraintScope.top()
        if self.location.x > right:
            self.location.x = right
            self.velocity.x *= -1
        if self.location.y > bottom:
            self.location.y = bottom
            self.velocity.y *= -1
        if self.location.x < left:
            self.location.x = left
            self.velocity.x *= -1
        if self.location.y < top:
            self.location.y = top
            self.velocity.y *= -1


# 模拟了重力，以及一般力，鼠标点击场景一下会施加一个平行的风力给小球
# class PhysicsScene(Scene):
#     def __init__(self, screen, config, clock):
#         super(PhysicsScene, self).__init__(screen, config, clock)
#         self.movers = []
#         for i in range(0, 5):
#             self.movers.append(Mover(vec2(random.randint(0, 800), 300), Rectangle(0, 0, 800, 600)))
#
#     def draw(self):
#
#         for m in self.movers:
#             gravity = vec2(0, 0.3)
#             gravity = gravity.mul(m.mass)
#             m.applyForce(gravity)
#
#
#             m.update()
#             m.edges()
#             m.display(self.screen)
#
#     def doMouseButtonDownEvent(self, MousePos, Button):
#         if Button == 1:
#             wind = vec2(0.2, 0)
#             for m in self.movers:
#                 m.applyForce(wind)


# 阻力与摩擦力
# class PhysicsScene(Scene):
#     def __init__(self, screen, config, clock):
#         super(PhysicsScene, self).__init__(screen, config, clock)
#         self.mover = Mover(vec2(400, 0), Rectangle(0, 0, 800, 600), 1)
#
#     def draw(self):
#         gravity = vec2(0, 0.3)
#         gravity = gravity.mul(self.mover.mass)
#         self.mover.applyForce(gravity)
#
#         self.mover.update()
#         self.mover.edges()
#         self.mover.display(self.screen)
#
#     def doMouseButtonDownEvent(self, MousePos, Button):
#         if Button == 1:
#             # 阻力
#             drag = self.mover.velocity.copy()
#             drag = drag.normal()
#             c = -4
#             speedSq = drag.len_square()
#             drag = drag.mulNum(c * speedSq)
#             self.mover.applyForce(drag)
#
#             # 摩擦力
#             # friction = self.mover.velocity.copy()
#             # friction = friction.normal()
#             # c = -0.1
#             # friction = friction.mul(c)
#             # self.mover.applyForce(friction)


class Attractor:
    def __init__(self, location):
        self.location = location
        self.mass = 20
        self.G = 1
        self.dragOffset = vec2()
        self.Events = IOEvent3()
        self.Events.appendEvent(ioEvent3Enum.key_D | ioEvent3Enum.keyDown, lambda: self.__X(True), 0)
        self.Events.appendEvent(ioEvent3Enum.key_A | ioEvent3Enum.keyDown, lambda: self.__X(False), 0)

    def __X(self, isAdd):
        if isAdd:
            self.location.x += 1
        else:
            self.location.x -= 10

    def attract(self, m):
        force = self.location - m.location
        d = force.len()
        d = constrain(d, 0, 8)
        force = force.normal()
        strength = (self.G * self.mass * m.mass) / (d * d)

        return force.mul(strength)

    def display(self, screen):
        loc = int(self.location.x), int(self.location.y)
        pygame.draw.circle(screen, (0, 255, 0), loc, self.mass * 2 + 14, 1)


class PhysicsScene(Scene):
    def __init__(self, screen, config, clock):
        super(PhysicsScene, self).__init__(screen, config, clock)
        self.m = Mover(vec2(500, 50), Rectangle(0, 0, 800, 600), 1)
        self.a = Attractor(vec2(400, 300))

    def draw(self):
        f = vec2(0.1, 0)
        self.m.applyForce(f)

        fa = self.a.attract(self.m)
        self.m.applyForce(fa)

        self.m.update()
        # self.a.update()

        self.a.display(self.screen)
        self.m.display(self.screen)

    def doKeyEvent(self, Key, Mod, Type, Unicode=None):
        self.a.Events.doKeyboardKeyDown(exKey(Key))


class body:
    def __init__(self, m, pos):
        self.vel = vec2()
        self.pos = pos
        self.mass = m
        self.acc = vec2()
        self.new_acc = vec2()

    def applyForce(self, force):
        self.new_acc += force.dev(self.mass)

    def update(self, dt):
        new_pos = self.pos + self.vel.mul(dt) + self.acc.mul(dt ** 2 * 0.5)
        _vel = self.vel + self.acc.mul(0.5 * dt)
        new_acc = self.new_acc
        self.new_acc = self.new_acc.mul(0)
        new_vel = _vel + new_acc.mul(dt * 0.5)
        self.pos = new_pos
        self.vel = new_vel
        self.acc = new_acc

    def edges(self, constraintScope):
        right = constraintScope.right()
        bottom = constraintScope.bottom()
        left = constraintScope.left()
        top = constraintScope.top()
        if self.pos.x > right:
            self.pos.x = right
            self.vel.x *= -0.8
        if self.pos.y > bottom:
            self.pos.y = bottom
            self.vel.y *= -0.8
        if self.pos.x < left:
            self.pos.x = left
            self.vel.x *= -0.8
        if self.pos.y < top:
            self.pos.y = top
            self.vel.y *= -0.8


class verletScene(Scene):
    def __init__(self, *args):
        super(verletScene, self).__init__(*args)
        self.caption = 'VerletSceneTest'
        self.m = body(1, vec2(100, 100))

    def setup(self):
        self.m.applyForce(vec2(0, 9.8).mul(self.m.mass))

    def doClockEvent(self, NowClock):
        # if self.FPS != 0:
        #     self.m.update(0.01)
        self.m.applyForce(vec2(0, 9.8))
        if self.mousePressed:
            self.m.applyForce(vec2(4, 0))
        self.m.update(0.1)
        self.m.edges(Rectangle(0, 0, self.width, self.height))

    def draw(self):
        self.Circle((self.m.pos.x, self.m.pos.y, 20), (0, 255, 0), 1)
        self.Lines((self.m.pos, self.m.vel + self.m.pos), (255, 255, 255), 1, 0)


class square:
    def __init__(self, i, area):
        self.ang_vel = 0
        self.vel = vec2()
        self.area = area
        self.acc_a = vec2()
        self.moi = i
        self.acc = vec2()
        self.angle = 0
        self.ang_acc = 0
        self.new_ang_acc = 0
        self.drag = 0.04

    def applyForce(self, force):
        v = vec2.fromPoint(self.area.barycenter(), force)
        self.new_ang_acc = 1 / self.moi * v.cross(force)
        # self.new_acc += force.dev(self.mass)

    def update(self, dt):
        new_angle = self.angle + self.ang_vel * dt + 0.5 * self.ang_acc * dt * dt
        # new_pos = self.pos + self.vel.mul(dt) + self.acc.mul(dt ** 2 * 0.5)
        _ang_vel = self.ang_vel + 0.5 * self.ang_acc * dt
        # _vel = self.vel + self.acc.mul(0.5 * dt)
        new_ang_acc = self.new_ang_acc
        # new_acc = self.new_acc
        self.new_ang_acc = 0
        # self.new_acc = self.new_acc.mul(0)
        new_ang_vel = _ang_vel + new_ang_acc * 0.5 * dt
        # new_vel = _vel + new_acc.mul(dt * 0.5)
        self.angle = new_angle
        # self.pos = new_pos
        self.ang_vel = new_ang_vel
        self.ang_vel = self.ang_vel * (1 - self.drag)
        # self.vel = new_vel
        self.ang_acc = new_ang_acc
        # self.acc = new_acc

    # def edges(self, constraintScope):
    #     right = constraintScope.right()
    #     bottom = constraintScope.bottom()
    #     left = constraintScope.left()
    #     top = constraintScope.top()
    #     if self.pos.x > right:
    #         self.pos.x = right
    #         self.vel.x *= -0.8
    #     if self.pos.y > bottom:
    #         self.pos.y = bottom
    #         self.vel.y *= -0.8
    #     if self.pos.x < left:
    #         self.pos.x = left
    #         self.vel.x *= -0.8
    #     if self.pos.y < top:
    #         self.pos.y = top
    #         self.vel.y *= -0.8


class verletSceneRotate(Scene):
    def __init__(self, *args):
        super(verletSceneRotate, self).__init__(*args)
        self.caption = 'VerletSceneRotateTest'
        self.m = square(100, Rectangle(300, 250, 200, 100))

    def setup(self):
        self.createTextElement()

    def doClockEvent(self, NowClock):
        self.m.update(0.01)

    def draw(self):
        self.push()
        self.rotate(400, 300, self.m.angle)
        self.Rect(self.m.area, (255, 255, 255), 1)
        self.pop()
        if self.mousePressed:
            self.m.applyForce(vec2(300, 300))
        self.getCreatedElement(0).setText(self.m.angle)

