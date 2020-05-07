from source.core.math.Vector import vec2


class Mass:
    def __init__(self, m):
        self.mass = m
        self.acceleration = vec2()
        self.velocity = vec2()
        self.local = vec2()

    def reset(self):
        self.acceleration = vec2()
        self.velocity = vec2()
        self.local = vec2()

    def applyForce(self, force):
        self.acceleration = force.dev(self.mass)

    def update(self, dt=1):
        self.velocity += self.acceleration.mul(dt)
        self.local += self.velocity.mul(dt)
        self.acceleration = self.acceleration.mul(0)

