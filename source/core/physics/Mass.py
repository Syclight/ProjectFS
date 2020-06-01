from source.core.math.Vector import vec2


class Mass:
    def __init__(self, m):
        self.mass = m
        self.acceleration = vec2()
        self.velocity = vec2()
        self.local = vec2()
        self.__new_acc = vec2()

    def reset(self):
        self.acceleration = vec2()
        self.velocity = vec2()
        self.local = vec2()

    def applyForce(self, force):
        self.__new_acc += force.dev(self.mass)

    def update(self, dt=0.4):
        new_pos = self.local + self.velocity.mul(dt) + self.acceleration.mul(dt ** 2 * 0.5)
        _vel = self.velocity + self.acceleration.mul(0.5 * dt)
        new_acc = self.__new_acc
        self.__new_acc = self.__new_acc.mul(0)
        new_vel = _vel + new_acc.mul(dt * 0.5)
        self.local = new_pos
        self.velocity = new_vel
        self.acceleration = new_acc

    # def applyForce(self, force):
    #     self.acceleration = force.dev(self.mass)
    #
    # def update(self, dt=1):
    #     self.velocity += self.acceleration.mul(dt)
    #     self.local += self.velocity.mul(dt)
    #     self.acceleration = self.acceleration.mul(0)

