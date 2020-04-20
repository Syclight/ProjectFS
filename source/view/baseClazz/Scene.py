class Scene:
    def __init__(self, *args):
        self.screen = args[0]
        self.config = args[1]
        self.startClock = args[2]
        self.paramList = []
        if isinstance(args[-1], list):
            self.paramList = args[-1]
        self.config.readConfig()
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.FPS = 0.0

        self.isReadyToEnter = False
        self.isEnter = False
        self.isEnd = False
        self.isReadyToEnd = False
        self.nextSceneNum = -1

        self.isFill = True
        self.fillColor = (0, 0, 0)

        self.mousePos = (0, 0)
        self.lastMousePos = (0, 0)
        self.mouseX, self.mouseY = 0, 0
        self.focus = None
        self.focus_onClick = 0

    def draw(self):
        pass

    def doMouseMotion(self, MouseRel, Buttons):
        pass

    def doMouseButtonDownEvent(self, Button):
        pass

    def doMouseButtonUpEvent(self, Button):
        pass

    def doKeyEvent(self, Key, Mod, Type, Unicode=None):
        pass

    def doKeyPressedEvent(self, KeyPressedList):
        pass

    def doClockEvent(self, NowClock):
        pass
