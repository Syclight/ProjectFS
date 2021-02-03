import math
from operator import eq

from source.core.assembly.IOEvent import getIOEvent3EnumByAscii
from source.core.assembly.Painter import Painter
from source.core.assembly.container import MiniQueue
from source.core.component.Console import Console
from source.core.component.Constructor import Constructor
from source.core.component.VideoPlayer import VideoPlay
from source.core.render.GameObjRender import gameObjRender
from source.util.ToolsFuc import InElement
from source.view.baseClazz.Element import Element
from source.view.sprite.Sprites import CursorSprite


class Scene(Constructor, Painter):
    def __init__(self, *args):
        self.screen = args[0]
        self.config = args[1]
        self.config.readConfig()
        self.startClock = args[2]
        self.mixer = args[3]
        self.systemConsole = args[4]
        self.paramList = []
        if isinstance(args[-1], list):
            self.paramList = args[-1]

        self.caption = None
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.screenRect = self.screen.get_rect()
        self.screenSize = (self.width, self.height)
        self.FPS = 0.0

        self.isReadyToEnter = False
        self.isEnter = False
        self.isEnd = False
        self.isReadyToEnd = False
        self.nextSceneNum = -1

        self.isFill = True
        self.fillColor = (0, 0, 0)
        self.frameCount = 0

        self.bgSurface = None
        self.bgSurfacePos = (0, 0)

        self.mousePos = (0, 0)
        self.lastMousePos = (0, 0)
        self.mouseX, self.mouseY = 0, 0
        self.focus = Element((0, 0, 0, 0))
        self.lastFocus = self.focus
        self.mouseVisible = True
        self.mouseLimited = False
        self.mousePressed = False
        self.keyPressed = False
        self.resetMouse = False

        self.useDefaultSetup = True
        self.useDefaultDraw = True
        self.useDefaultMouseHeading = True
        self.useDefaultKeyHeading = True
        self.useDefaultClock = True

        self.letDefaultDrawLast = False

        self.setupSystemConsole = True
        self.__recordMouseZIndexBeforeSystemConsoleShow = 0
        self.mouseSprite = CursorSprite()

        self.__focus_onClick = 0

        # 数据容器
        self.keyboardEventQueue = MiniQueue(1000)
        self.systemConsole.msgQueue = self.keyboardEventQueue

        self.render = gameObjRender()
        self.videoPlayer = VideoPlay()

        Constructor.__init__(self, self.render, self.screen.get_rect())
        Painter.__init__(self, self.screen)

    # 默认的处理函数，由useDefault开头的变量控制要不要启用
    # 默认为开启

    def __setup(self):
        self.render.add(self.mouseSprite)
        if self.setupSystemConsole:
            self.render.add(self.systemConsole)
        self.render.close()

    def __draw(self):
        self.render.render(self.screen)

    def __doMouseMotive(self, MouseRel, Buttons):
        for e in self.render.eventHandingList():
            if not e.active:
                continue
            if InElement(self.mousePos, e):
                if isinstance(e, Element):
                    e.mouseLastPos = (self.lastMousePos[0] - e.area.x, self.lastMousePos[1] - e.area.y)
                    e.mousePos = (self.mouseX - e.area.x, self.mouseY - e.area.y)
                e.mouseButtons = Buttons
                e.mouseRel = MouseRel
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
            self.__focus_onClick = 0

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

    def __doMouseButtonDownEvent(self, Button):
        if Button == 1:  # 鼠标左键
            if InElement(self.mousePos, self.focus) and self.focus.EventsHadDo.hadDoMouseRightKeyUp:
                self.__focus_onClick = 1
                self.focus.Events.doMouseLeftKeyDown()
                self.focus.EventsHadDo.hadDoMouseLeftKeyDown = True
                self.focus.EventsHadDo.hadDoMouseLeftKeyUp = False
        if Button == 2:  # 鼠标中键
            if InElement(self.mousePos, self.focus) and self.focus.EventsHadDo.hadDoMouseMidKeyUp:
                self.focus.Events.doMouseMidKeyDown()
                self.focus.EventsHadDo.hadDoMouseMidKeyDown = True
                self.focus.EventsHadDo.hadDoMouseMidKeyUp = False
        if Button == 3:  # 鼠标右键键
            if InElement(self.mousePos, self.focus) and self.focus.EventsHadDo.hadDoMouseLeftKeyUp:
                self.focus.Events.doMouseRightKeyDown()
                self.focus.EventsHadDo.hadDoMouseRightKeyDown = True
                self.focus.EventsHadDo.hadDoMouseRightKeyUp = False
        if Button == 4:  # 滚轮向上
            if InElement(self.mousePos, self.focus):
                self.focus.Events.doMouserRollUp()
        if Button == 5:  # 滚轮向下
            if InElement(self.mousePos, self.focus):
                self.focus.Events.doMouserRollDown()

    def __doMouseButtonUpEvent(self, Button):
        if Button == 1:  # 鼠标左键
            if InElement(self.mousePos, self.focus) and self.focus.EventsHadDo.hadDoMouseLeftKeyDown:
                self.focus.Events.doMouseLeftKeyUp()
                self.focus.EventsHadDo.hadDoMouseLeftKeyDown = False
                self.focus.EventsHadDo.hadDoMouseLeftKeyUp = True
                if self.__focus_onClick == 1:  # click 事件
                    self.focus.Events.doMouseLeftKeyClick()
                    self.focus.EventsHadDo.hadDoMouseLeftKeyClick = True
                self.__focus_onClick = 0
        if Button == 2:  # 鼠标中键
            if InElement(self.mousePos, self.focus) and self.focus.EventsHadDo.hadDoMouseMidKeyDown:
                self.focus.Events.doMouseMidKeyUp()
                self.focus.EventsHadDo.hadDoMouseMidKeyDown = False
                self.focus.EventsHadDo.hadDoMouseMidKeyUp = True
        if Button == 3:  # 鼠标右键
            if InElement(self.mousePos, self.focus) and self.focus.EventsHadDo.hadDoMouseRightKeyDown:
                self.focus.Events.doMouseRightKeyUp()
                self.focus.EventsHadDo.hadDoMouseRightKeyDown = False
                self.focus.EventsHadDo.hadDoMouseRightKeyUp = True

    def __doClockEvent(self, NowClock):
        pass

    def __doKeyEvent(self, Key, Mod, Type, Unicode=None):
        if Type == 0:  # 按下
            self.focus.Events.doKeyDown(getIOEvent3EnumByAscii(Key))
        if Type == 1:  # 松开
            self.focus.Events.doKeyUp(getIOEvent3EnumByAscii(Key))

    def __doKeyPressedEvent(self, KeyPressedList):
        pass

    #  super_开头的是gameApp调用的方法，禁止重写！

    def super_setup(self):
        if self.useDefaultSetup:
            self.__setup()

        self.setup()

    def super_draw(self):
        if self.bgSurface:
            self.screen.blit(self.bgSurface, self.bgSurfacePos)
        if self.letDefaultDrawLast:
            self.draw()
        if self.useDefaultDraw:
            self.__draw()
        if not self.letDefaultDrawLast:
            self.draw()

    def super_doMouseMotion(self, MouseRel, Buttons):
        if self.useDefaultMouseHeading:
            self.__doMouseMotive(MouseRel, Buttons)

        self.doMouseMotion(MouseRel, Buttons)

    def super_doMouseButtonDownEvent(self, Button):
        if self.useDefaultMouseHeading:
            self.__doMouseButtonDownEvent(Button)

        self.doMouseButtonDownEvent(Button)

    def super_doMouseButtonUpEvent(self, Button):
        if self.useDefaultMouseHeading:
            self.__doMouseButtonUpEvent(Button)

        self.doMouseButtonUpEvent(Button)

    def super_doClockEvent(self, NowClock):
        if self.useDefaultClock:
            self.__doClockEvent(NowClock)

        self.doClockEvent(NowClock)

    def super_doKeyEvent(self, Key, Mod, Type, Unicode=None):
        if self.useDefaultKeyHeading:
            self.__doKeyEvent(Key, Mod, Type, Unicode)

        if Key == 282 and Type == 0 and Mod == 0:
            visual = self.systemConsole.visual
            active = self.systemConsole.active
            if not visual and not active:
                self.__recordMouseZIndexBeforeSystemConsoleShow = self.mouseSprite.zIndex
                self.mouseSprite.zIndex = self.systemConsole.zIndex
            if visual and active:
                self.mouseSprite.zIndex = self.__recordMouseZIndexBeforeSystemConsoleShow
            self.systemConsole.visual = not self.systemConsole.visual
            self.systemConsole.active = not self.systemConsole.active
            self.focus = self.systemConsole

        if Type == 2:
            self.keyPressed = True
        else:
            self.keyPressed = False
        self.doKeyEvent(Key, Mod, Type, Unicode)

    def super_doKeyPressedEvent(self, KeyPressedList):
        if self.useDefaultKeyHeading:
            self.__doKeyPressedEvent(KeyPressedList)
        self.keyPressed = True
        self.doKeyPressedEvent(KeyPressedList)

    # 可以重写的方法

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
