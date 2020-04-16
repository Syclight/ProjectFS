class Scene:
    def __init__(self, *args):
        self.screen = args[0]
        self.config = args[1]
        self.startClock = args[2]
        self.paramList = []
        if isinstance(args[-1], list):
            self.paramList = args[-1]
        self.config.readConfig()

        self.isReadyToEnter = False
        self.isEnter = False
        self.isEnd = False
        self.isReadyToEnd = False
        self.nextSceneNum = -1

        self.mousePos = (0, 0)
        self.lastMousePos = (0, 0)
        self.focus = None
        self.focus_onClick = 0

    def draw(self):
        pass

    def doMouseMotion(self, MousePos, MouseRel, Buttons):
        pass

    def doMouseButtonDownEvent(self, MousePos, Button):
        pass

    def doMouseButtonUpEvent(self, MousePos, Button):
        pass

    def doKeyEvent(self, Key, Mod, Type, Unicode=None):
        pass

    def doKeyPressedEvent(self, KeyPressedList):
        pass

    def doClockEvent(self, NowClock):
        pass
