import random
import pygame

from source.controller.assembly.Shape import Rectangle
from source.util.Math2d import vec2
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
        f = force.mulNum(1 / self.mass)
        self.acceleration += f

    def update(self):
        self.velocity += self.acceleration
        self.location += self.velocity
        self.acceleration = self.acceleration.mulNum(0)

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
            self.location.y *= -1


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
#             gravity = gravity.mulNum(m.mass)
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
#         gravity = gravity.mulNum(self.mover.mass)
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
#             # friction = friction.mulNum(c)
#             # self.mover.applyForce(friction)


class PhysicsScene(Scene):
    def __init__(self, screen, config, clock):
        super(PhysicsScene, self).__init__(screen, config, clock)
        self.mover = Mover(vec2(400, 0), Rectangle(0, 0, 800, 600), 1)

    def draw(self):
        gravity = vec2(0, 0.3)
        gravity = gravity.mulNum(self.mover.mass)
        self.mover.applyForce(gravity)

        self.mover.update()
        self.mover.edges()
        self.mover.display(self.screen)
