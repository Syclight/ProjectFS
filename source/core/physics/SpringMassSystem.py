from source.core.math.Vector import vec2
from source.core.physics.Mass import Mass
from source.core.physics.Spring import Spring


class SMSystem:
    LINE, GRID, CROSS, GRID_CROSS = 0, 1, 2, 3

    def __init__(self, *args):
        """0 质点的数量，1 质点的质量，2 劲度系数K，

        3 弹簧长度，4 弹簧阻力系数，5 重力加速度，

        6 空气阻力，7 地面斥力，8 地面摩擦力阻力，

        9 地面引力，10 地面高度"""

        self.__mod = self.LINE

        self.massSum = args[0]
        self.massM = args[1]
        self.K = args[2]
        self.springLength = args[3]
        self.springFriction = args[4]
        self.g = args[5]

        self.airFriction = args[6]
        self.groundRepulsion = args[7]
        self.groundFriction = args[8]
        self.groundAbsorption = args[9]
        self.groundHeight = args[10]

        self.masses = list()
        self.springs = list()
        self.connections = list()

    def __createModel_LINE(self):
        for i in range(self.massSum):
            m = Mass(self.massM)
            m.local = vec2(i * self.springLength, 400)
            self.masses.append(m)
            if i > 0:
                self.springs.append(
                    Spring(self.masses[i - 1], self.masses[i], self.K, self.springLength, self.springFriction))

    def getLocal(self):
        lis = []
        for m in self.masses:
            lis.append(m.local)
        return lis

    def createModel(self):
        if self.__mod == self.LINE:
            self.__createModel_LINE()

    def setMod(self, mod):
        self.__mod = mod

    def setConnections(self, *args):
        for p in args:
            self.connections.append(p)

    def simulate(self, dt=1):
        for i in range(self.massSum):
            self.masses[i].update(dt)

        for p in self.connections:  # (index, vec2:vel)
            index = p[0]
            pos = p[1].mul(dt)
            if pos.y > self.groundHeight:
                pos.y = self.groundHeight
                p[1].y = 0

            self.masses[index].local = pos
            self.masses[index].velocity = p[1]

    def getMass(self, index):
        return self.masses[index]

    def operate(self, dt=1):
        self.resetMassForce()
        self.execute()
        self.simulate(dt)

    def execute(self):
        for i in range(self.massSum - 1):
            self.springs[i].execute()

        for i in range(self.massSum):
            self.masses[i].applyForce(self.g.mul(self.masses[i].mass))
            self.masses[i].applyForce(self.masses[i].velocity.negate().mul(self.airFriction))

            if self.masses[i].local.y > self.groundHeight:
                v = self.masses[i].velocity
                v.y = 0

                self.masses[i].applyForce(v.negate().mul(self.groundFriction))
                v = self.masses[i].velocity
                v.x = 0

                if v.y < 0:
                    self.masses[i].applyForce(v.negate().mul(self.groundAbsorption))

                f = vec2(0, self.groundRepulsion).mul(self.masses[i].local.y - self.groundHeight)
                self.masses[i].applyForce(f)

    def resetMassForce(self):
        for i in range(self.massSum):
            self.masses[i].reset()
