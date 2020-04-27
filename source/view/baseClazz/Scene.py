from operator import eq


from source.core.render.GameObjRender import gameObjRender
from source.util.ToolsFuc import InElement
from source.view.baseClazz.Element import Element


class Scene:
    def __init__(self, *args):
        self.screen = args[0]
        self.config = args[1]
        self.config.readConfig()
        self.startClock = args[2]
        self.paramList = []
        if isinstance(args[-1], list):
            self.paramList = args[-1]

        #Config
        self.config_isAA = False
        self.config_volBGM = 0.0
        self.config_volSound = 0.0
        self.config_frameRate = 0

        self.caption = None
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
        self.frameCount = 0

        self.mousePos = (0, 0)
        self.lastMousePos = (0, 0)
        self.mouseX, self.mouseY = 0, 0
        self.focus = Element((0, 0, 0, 0))
        self.lastFocus = self.focus
        self.mousePressed = False
        self.keyPressed = False

        self.__focus_onClick = 0

        self.render = gameObjRender()

    def super_setup(self):
        self.setup()

    def super_draw(self):
        self.draw()

    def super_doMouseMotion(self, MouseRel, Buttons):
        for e in self.render.eventHandingList():
            if InElement(self.mousePos, e):
                if InElement(self.lastMousePos, e):
                    e.Events.doMouseMotion()

                if self.focus != e:
                    self.lastFocus = self.focus
                    # print('失去焦点元素：', self.focus.area, '\n鼠标位置：', self.mousePos)
                    # print('确定焦点元素：', e.area, '\n鼠标位置：', self.mousePos)
                self.focus = e

                if eq(Buttons, (0, 0, 0)) and not self.focus.EventsHadDo.hadDoMouseIn:
                    self.focus.Events.doMouseIn()
                    self.focus.EventsHadDo.hadDoMouseIn = True
                    self.focus.EventsHadDo.hadDoMouseOut = False
                break

        if not InElement(self.mousePos, self.focus):
            self.lastFocus = self.focus
            self.focus = Element((0, 0, 0, 0))

        if self.lastFocus.EventsHadDo.hadDoMouseIn:
            self.lastFocus.Events.doMouseOut()
            self.lastFocus.EventsHadDo.hadDoMouseOut = True
            self.lastFocus.EventsHadDo.hadDoMouseIn = False

        if self.lastFocus.EventsHadDo.hadDoMouseLeftKeyDown:
            self.lastFocus.Events.doMouseLeftKeyUp()
            self.lastFocus.EventsHadDo.hadDoMouseLeftKeyDown = False
            self.lastFocus.EventsHadDo.hadDoMouseLeftKeyUp = True

        if self.lastFocus.EventsHadDo.hadDoMouseRightKeyDown:
            self.lastFocus.Events.doMouseRightKeyUp()
            self.lastFocus.EventsHadDo.hadDoMouseRightKeyDown = False
            self.lastFocus.EventsHadDo.hadDoMouseRightKeyUp = True

        # 最后执行重写的方法
        self.doMouseMotion(MouseRel, Buttons)

    def super_doMouseButtonDownEvent(self, Button):
        if Button == 1:  # 鼠标左键
            if InElement(self.mousePos, self.focus):
                self.__focus_onClick = 1
                self.focus.Events.doMouseLeftKeyDown()
                self.focus.EventsHadDo.hadDoMouseLeftKeyDown = True
                self.focus.EventsHadDo.hadDoMouseLeftKeyUp = False
        if Button == 2:  # 鼠标中键
            if InElement(self.mousePos, self.focus):
                self.focus.Events.doMouseMidKeyDown()
                self.focus.EventsHadDo.hadDoMouseMidKeyDown = True
                self.focus.EventsHadDo.hadDoMouseMidKeyUp = False
        if Button == 3:  # 鼠标右键键
            if InElement(self.mousePos, self.focus):
                self.focus.Events.doMouseRightKeyDown()
                self.focus.EventsHadDo.hadDoMouseRightKeyDown = True
                self.focus.EventsHadDo.hadDoMouseRightKeyUp = False

        # 最后执行重写的方法
        self.doMouseButtonDownEvent(Button)

    def super_doMouseButtonUpEvent(self, Button):
        if Button == 1:  # 鼠标左键
            if InElement(self.mousePos, self.focus):
                self.focus.Events.doMouseLeftKeyUp()
                self.focus.EventsHadDo.hadDoMouseLeftKeyDown = False
                self.focus.EventsHadDo.hadDoMouseLeftKeyUp = True
                if self.__focus_onClick == 1:  # click 事件
                    self.focus.Events.doMouseLeftKeyClick()
                    self.focus.EventsHadDo.hadDoMouseLeftKeyClick = True
                self.__focus_onClick = 0
        if Button == 2:  # 鼠标中键
            if InElement(self.mousePos, self.focus):
                self.focus.Events.doMouseMidKeyUp()
                self.focus.EventsHadDo.hadDoMouseMidKeyDown = False
                self.focus.EventsHadDo.hadDoMouseMidKeyUp = True
        if Button == 3:  # 鼠标右键
            if InElement(self.mousePos, self.focus):
                self.focus.Events.doMouseRightKeyUp()
                self.focus.EventsHadDo.hadDoMouseRightKeyDown = False
                self.focus.EventsHadDo.hadDoMouseRightKeyUp = True

        # 最后执行重写的方法
        self.doMouseButtonUpEvent(Button)

    def super_doClockEvent(self, NowClock):
        self.doClockEvent(NowClock)

    def super_doKeyEvent(self, Key, Mod, Type, Unicode=None):
        if Type == 2:
            self.keyPressed = True
        else:
            self.keyPressed = False

        self.doKeyEvent(Key, Mod, Type, Unicode)

    def super_doKeyPressedEvent(self, KeyPressedList):
        self.keyPressed = True
        self.doKeyPressedEvent(KeyPressedList)

    # 需要重写的方法
    def setup(self):
        pass

    def draw(self):
        pass

    def doMouseMotion(self, MouseRel, Buttons):
        pass

    def doMouseButtonDownEvent(self, Button):
        pass

    def doMouseButtonUpEvent(self, Button):
        pass

    def doKeyEvent(self, Key, Mod, Type, Unicode):
        pass

    def doKeyPressedEvent(self, KeyPressedList):
        pass

    def doClockEvent(self, NowClock):
        pass
