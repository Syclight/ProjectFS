class CVState:
    ready = 0
    active = 1
    wait = 2
    running = 3
    dead = 4

    def returnName(self, num):
        if num == self.ready:
            return 'ready'
        if num == self.active:
            return 'active'
        if num == self.wait:
            return 'wait'
        if num == self.running:
            return 'running'
        if num == self.dead:
            return 'dead'


class ConsoleVariable:
    counter = 0

    def __init__(self):
        self.name = 'ConsoleVariable' + str(self.counter)
        self.val = 0
        self.describe = 'null'
        self.fuc = lambda: ()
        self.__state = CVState.ready
        self.counter += 1

    def __str__(self):
        return self.name + ': \n' + self.describe + '\n' + 'state: ' + CVState.returnName(self.__state)

    def changeSate(self, state):
        self.__state = state
