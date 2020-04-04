class Scene:
    def __init__(self, screen, config, startClock, paramList=None):
        self.screen = screen
        self.config = config
        self.config.readConfig()
        self.paramList = paramList

        self.isReadyToEnter = False
        self.isEnter = False
        self.isEnd = False
        self.isReadyToEnd = False
        self.nextSceneNum = -1

        self.mousePos = (0, 0)
        self.lastMousePos = (0, 0)
        self.focus = None
        self.focus_onClick = 0

        self.startClock = startClock

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
