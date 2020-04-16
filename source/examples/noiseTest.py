from source.controller.assembly.Painter import Painter
from source.core.math.Math2d import point2
from source.core.math.Noise import noise
from source.view.baseClazz.Scene import Scene


class noiseTestScene(Scene):
    def __init__(self, *args):
        super(noiseTestScene, self).__init__(*args)
        self.noiseScale = 0.02

    def draw(self):
        for x in range(0, 800):
            noiseVal = noise((self.mousePos[0] + x) * self.noiseScale, self.mousePos[1] * self.noiseScale)
            Painter(self.screen).Lines([point2(x, self.mousePos[1] + noiseVal * 80), point2(x, 600)],
                                       (noiseVal * 255, noiseVal * 255, noiseVal * 255), 1, 0)

    def doMouseMotion(self, MousePos, MouseRel, Buttons):
        self.mousePos = MousePos
