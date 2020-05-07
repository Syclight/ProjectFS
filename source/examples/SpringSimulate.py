from source.core.math.Vector import vec2
from source.core.physics.Mass import Mass
from source.core.physics.Spring import Spring
from source.core.physics.SpringMassSystem import SMSystem
from source.view.baseClazz.Scene import Scene


class SpringSimulateScene(Scene):
    def __init__(self, *args):
        super(SpringSimulateScene, self).__init__(*args)
        self.m1, self.m2, self.m3, self.m4 = Mass(40), Mass(40), Mass(40), Mass(40)
        self.m5 = Mass(40)
        self.spring1 = Spring(self.m1, self.m2, 100, 0.8, 1)
        self.spring2 = Spring(self.m1, self.m3, 100, 0.8, 1)
        self.spring3 = Spring(self.m2, self.m4, 100, 0.8, 1)
        self.spring4 = Spring(self.m3, self.m4, 100, 0.8, 1)

        self.spring5 = Spring(self.m2, self.m5, 100, 0.8, 1)
        self.spring6 = Spring(self.m4, self.m5, 100, 0.8, 1)

        self.target = self.m5

    def setup(self):
        self.createTextElement('spring length1:')
        self.createTextElement('spring length2:')

        self.m1.local = vec2(100, 100)
        self.m2.local = vec2(200, 100)
        self.m3.local = vec2(100, 200)
        self.m4.local = vec2(200, 200)

        self.m5.local = vec2(280, 150)

    def draw(self):
        self.Lines((self.spring1.beginMass.local, self.spring1.endMass.local), (255, 255, 255), 1, 0, 1)
        self.Lines((self.spring2.beginMass.local, self.spring2.endMass.local), (255, 0, 0), 1, 0, 1)
        self.Lines((self.spring3.beginMass.local, self.spring3.endMass.local), (0, 255, 0), 1, 0, 1)
        self.Lines((self.spring4.beginMass.local, self.spring4.endMass.local), (0, 0, 255), 1, 0, 1)
        self.Lines((self.spring5.beginMass.local, self.spring5.endMass.local), (0, 255, 255), 1, 0, 1)
        self.Lines((self.spring6.beginMass.local, self.spring6.endMass.local), (255, 0, 255), 1, 0, 1)
        self.Circle((self.target.local.x, self.target.local.y, 1), (255, 255, 0), 1)

    def doClockEvent(self, NowClock):
        self.spring1.execute()
        self.spring2.execute()
        self.spring3.execute()
        self.spring4.execute()
        self.spring5.execute()
        self.spring6.execute()

        self.getCreatedElement(0).setText(
            'spring length1:' + str(self.spring1.endMass.local.dist(self.spring1.beginMass.local)))
        self.getCreatedElement(1).setText(
            'spring length2:' + str(self.spring2.endMass.local.dist(self.spring2.beginMass.local)))

    # def doMouseButtonDownEvent(self, Button):
    #     self.spring.endMass.local += vec2(100, 0)

    def doMouseMotion(self, MouseRel, Buttons):
        if Buttons == (1, 0, 0):
            self.target.local.x += MouseRel[0]
            self.target.local.y += MouseRel[1]


class SpringMassSystemTestScene(Scene):
    def __init__(self, *args):
        super(SpringMassSystemTestScene, self).__init__(*args)
        self.springMassSys = SMSystem(10,
                                      2.0,
                                      0.9, 40, 0.2,
                                      vec2(0, 0.098),
                                      2, 2, 1, 2, 700)

    def setup(self):
        self.springMassSys.createModel()
        self.springMassSys.setConnections((0, vec2(0, 0)))

    def draw(self):
        self.Lines(self.springMassSys.getLocal(), (255, 255, 255), 1, 0, 1)

    def doClockEvent(self, NowClock):
        self.springMassSys.simulate()

    def doMouseButtonDownEvent(self, Button):
        self.springMassSys.execute()
