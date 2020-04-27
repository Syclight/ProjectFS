import pygame

from source.const.Const import gl_Font
from source.view.baseClazz.Scene import Scene
from source.view.element.Elements import TextElement


class canvasTest(Scene):
    def __init__(self, *args):
        super(canvasTest, self).__init__(*args)
        # self.can = canvas(color(0, 0, 0), vec2(800, 600))
        # self.brush = brush(self.can, (255, 255, 255, 0.5), 1)
        # self.painter = Painter(self.can.surface())
        self.blend = pygame.Surface((300, 300)).convert()
        self.blend.fill((255, 255, 255))
        self.blend.set_alpha(80)
        self.sceneCanvas = pygame.Surface((self.width, self.height))
        self.sceneCanvas.fill((255, 255, 255))
        self.sceneCanvas.set_alpha(100)
        self.__E_FPS = TextElement(pygame.Rect(self.width - 80, 0, 80, 20), 'FPS:', gl_Font, 18, (0, 255, 0), 1)

    def draw(self):
        # self.can.fill(color(0, 0, 0))
        # self.brush.drawLine((0, 0), (700, 500))
        # self.painter.Lines([point2(), point2(500, 700)], (255, 255, 255, 100), 1, 0)
        #
        # self.__E_FPS.draw(self.can.surface())
        # self.screen.blit(self.can.surface(), (0, 0))
        self.screen.blit(self.blend, (0, 0))
        self.screen.blit(self.sceneCanvas, (0, 0))
        self.__E_FPS.draw(self.screen)

    def doClockEvent(self, NowClock):
        fps = 'FPS:' + str(self.FPS)
        self.__E_FPS.setText(fps)


class water2d(Scene):
    def __init__(self, *args):
        super(water2d, self).__init__(*args)
        self.sceneCanvas = pygame.Surface((200, 200))
        self.cols, self.rows = 200, 200
        self.current = [[0 for i in range(self.cols)] for j in range(self.rows)]
        self.previous = [[0 for i in range(self.cols)] for j in range(self.rows)]
        # self.background(220, 220, 220)
        self.dampening = 0.9
        # self.previous[100][100] = 255

    def draw(self):
        self.sceneCanvas.fill((0, 0, 0))
        for i in range(1, self.rows - 1):
            for j in range(1, self.cols - 1):
                self.current[i][j] = (self.previous[i - 1][j] + self.previous[i + 1][j] + self.previous[i][j - 1] +
                                      self.previous[i][j + 1]) / 2 - self.current[i][j]
                self.current[i][j] = self.current[i][j] * self.dampening
                gray = self.current[i][j]
                try:
                    self.sceneCanvas.set_at((i, j), (round(200 * gray), round(200 * gray), round(200 * gray)))
                except TypeError:
                    pass
                    # print(gray)
                    # print(round(255 * gray), round(255 * gray), round(255 * gray))

        self.previous, self.current = self.current, self.previous
        self.screen.blit(self.sceneCanvas, (0, 0))

    def doClockEvent(self, NowClock):
        pass

    def doMouseButtonDownEvent(self, Button):
        if Button == 1:
            if 0 < self.mouseX < 200 and 0 < self.mouseY < 200:
                self.previous[self.mouseX][self.mouseY] = 255

    # def doMouseMotion(self, MouseRel, Buttons):
    #     if Buttons eq (1, 0, 0):
    #         self.previous[self.mouseX][self.mouseY] = 255

