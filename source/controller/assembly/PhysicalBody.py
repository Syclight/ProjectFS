class physicalBody:
    def __init__(self, m, initVel):
        self.m = m
        self.initVel = initVel

    def update(self, force):
        pass


class rigidBody(physicalBody):
    def __init__(self, activityScope, g, m, initVel):
        super(rigidBody, self).__init__(m, initVel)
        self.activityScope = activityScope
        self.g = g

    def update(self, collideArea, force):
        if collideArea.x <= self.activityScope.x:
            collideArea.x = self.activityScope.x
        elif collideArea.x >= self.activityScope.x + self.activityScope.w - collideArea.w:
            collideArea.x = self.activityScope.x + self.activityScope.w - collideArea.w
        else:
            if not force.isZero():
                collideArea.x += self.initVel + 0.5 * (force.x / self.m)

        if collideArea.y <= self.activityScope.y:
            collideArea.y = self.activityScope.y
        elif collideArea.y >= self.activityScope.y + self.activityScope.h - collideArea.h:
            collideArea.y = self.activityScope.y + self.activityScope.h - collideArea.h
        else:
            collideArea.y += self.initVel + 0.5 * self.g
            if not force.isZero():
                collideArea.y += self.initVel + 0.5 * (force.y / self.m)
