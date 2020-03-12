Sum = 15

mouseIn = '0000'
mouseOut = '0001'
mouseLeftKeyDown = '1000'
mouseLeftKeyUp = '1001'
mouseLeftKeyClick = '1002'
mouseRightKeyDown = '0010'
mouseRightKeyUp = '0011'
mouseRightKeyClick = '0012'
mouseMidKeyDown = '0100'
mouseMidKeyUp = '0101'
mouseMidKeyClick = '0102'
mouseDoubleClick = '1003'


class IOEvent:
    def doMouseIn(self):
        pass

    def doMouseOut(self):
        pass

    def doMouseLeftKeyUp(self):
        pass

    def doMouseLeftKeyDown(self):
        pass

    def doMouseLeftKeyClick(self):
        pass

    def doMouseRightKeyUp(self):
        pass

    def doMouseRightKeyDown(self):
        pass

    def doMouseRightKeyClick(self):
        pass

    def doMouseMidKeyUp(self):
        pass

    def doMouseMidKeyDown(self):
        pass

    def doMouseMidKeyClick(self):
        pass

    def doDoubleClick(self):
        pass

    def doKeyboardKeyUp(self, Key):
        pass

    def doKeyboardKeyDown(self, Key):
        pass

    def doKeyboardKeyDowning(self, Key):
        pass


class IOEvent2:
    mouseIn = None
    mouseOut = None
    mouseLeftKeyUp = None
    mouseLeftKeyDown = None
    mouseLeftKeyClick = None
    mouseRightKeyUp = None
    mouseRightKeyDown = None
    mouseRightKeyClick = None
    mouseMidKeyUp = None
    mouseMidKeyDown = None
    mouseMidKeyClick = None
    doubleClick = None
    keyboardKeyUp = None
    keyboardKeyDown = None
    keyboardKeyDowning = None

    def __init__(self):
        self.mouseIn = []
        self.mouseOut = []
        self.mouseLeftKeyUp = []
        self.mouseLeftKeyDown = []
        self.mouseLeftKeyClick = []
        self.mouseRightKeyUp = []
        self.mouseRightKeyDown = []
        self.mouseRightKeyClick = []
        self.mouseMidKeyUp = []
        self.mouseMidKeyDown = []
        self.mouseMidKeyClick = []
        self.doubleClick = []
        self.keyboardKeyUp = {}
        self.keyboardKeyDown = {}
        self.keyboardKeyDowning = {}

    def doMouseIn(self):
        if len(self.mouseIn) > 0:
            for e in self.mouseIn:
                e()

    def doMouseOut(self):
        if len(self.mouseOut) > 0:
            for e in self.mouseOut:
                e()

    def doMouseLeftKeyUp(self):
        if len(self.mouseLeftKeyUp) > 0:
            for e in self.mouseLeftKeyUp:
                e()

    def doMouseLeftKeyDown(self):
        if len(self.mouseLeftKeyDown) > 0:
            for e in self.mouseLeftKeyDown:
                e()

    def doMouseLeftKeyClick(self):
        if len(self.mouseLeftKeyClick) > 0:
            for e in self.mouseLeftKeyClick:
                e()

    def doMouseRightKeyUp(self):
        if len(self.mouseRightKeyUp) > 0:
            for e in self.mouseRightKeyUp:
                e()

    def doMouseRightKeyDown(self):
        if len(self.mouseRightKeyDown) > 0:
            for e in self.mouseRightKeyDown:
                e()

    def doMouseRightKeyClick(self):
        if len(self.mouseRightKeyClick) > 0:
            for e in self.mouseRightKeyClick:
                e()

    def doMouseMidKeyUp(self):
        if len(self.mouseMidKeyUp) > 0:
            for e in self.mouseMidKeyUp:
                e()

    def doMouseMidKeyDown(self):
        if len(self.mouseMidKeyDown) > 0:
            for e in self.mouseMidKeyDown:
                e()

    def doMouseMidKeyClick(self):
        if len(self.mouseMidKeyClick) > 0:
            for e in self.mouseMidKeyClick:
                e()

    def doDoubleClick(self):
        if len(self.doubleClick) > 0:
            for e in self.doubleClick:
                e()

    def addKeyboardKeyUpEvent(self, Key, fuc):
        if not self.keyboardKeyUp:
            self.keyboardKeyUp[Key] = []
        self.keyboardKeyUp[Key].append(fuc)

    def doKeyboardKeyUp(self, Key):
        eventList = self.keyboardKeyUp[Key]
        if len(eventList) > 0:
            for e in eventList:
                e()

    def addKeyboardKeyDownEvent(self, Key, fuc):
        if not self.keyboardKeyDown:
            self.keyboardKeyDown[Key] = []
        self.keyboardKeyDown[Key].append(fuc)

    def doKeyboardKeyDown(self, Key):
        eventList = self.keyboardKeyDown[Key]
        if len(eventList) > 0:
            for e in eventList:
                e()

    def addKeyboardKeyDowningEvent(self, Key, fuc):
        if not self.keyboardKeyDowning:
            self.keyboardKeyDowning[Key] = []
        self.keyboardKeyDowning[Key].append(fuc)

    def doKeyboardKeyDowning(self, Key):
        eventList = self.keyboardKeyDowning[Key]
        if len(eventList) > 0:
            for e in eventList:
                e()


class IOEvent3:
    def __init__(self):
        self.__Events = {'0000': [], '0001': [], '1000': [], '1001': [], '1002': [], '0010': [], '0011': [], '0012': [],
                         '0100': [], '0101': [], '0102': [], '1003': []}
        self.__MouseEnum = [mouseIn, mouseOut, mouseLeftKeyDown, mouseLeftKeyUp, mouseLeftKeyClick, mouseRightKeyDown,
                            mouseRightKeyUp, mouseRightKeyClick, mouseMidKeyDown, mouseMidKeyUp, mouseMidKeyClick,
                            mouseDoubleClick]
        self.__KeyEnum = []
        self.__EventsKB = {}
        self.__EventsContain = 0

    def appendEvent(self, ioEvent3Enum, fuc):
        if ioEvent3Enum not in self.__MouseEnum and ioEvent3Enum not in self.__KeyEnum:
            return
        if ioEvent3Enum in self.__MouseEnum:
            self.__Events[ioEvent3Enum].append(fuc)
        if ioEvent3Enum in self.__KeyEnum:
            self.__EventsKB[ioEvent3Enum].apped(fuc)
        self.__EventsContain += 1

    def getSize(self):
        return self.__EventsContain

    def doEvents(self, ioEvent3Enum):
        if ioEvent3Enum not in self.__MouseEnum and ioEvent3Enum not in self.__KeyEnum:
            return
        _list = self.__Events[ioEvent3Enum]
        if len(_list) > 0:
            for e in _list:
                e()

    def doMouseIn(self):
        _list = self.__Events[mouseIn]
        if len(_list) > 0:
            for e in _list:
                e()

    def doMouseOut(self):
        _list = self.__Events[mouseOut]
        if len(_list) > 0:
            for e in _list:
                e()

    def doMouseLeftKeyUp(self):
        _list = self.__Events[mouseLeftKeyUp]
        if len(_list) > 0:
            for e in _list:
                e()

    def doMouseLeftKeyDown(self):
        _list = self.__Events[mouseLeftKeyDown]
        if len(_list) > 0:
            for e in _list:
                e()

    def doMouseLeftKeyClick(self):
        _list = self.__Events[mouseLeftKeyClick]
        if len(_list) > 0:
            for e in _list:
                e()

    def doMouseRightKeyUp(self):
        _list = self.__Events[mouseRightKeyUp]
        if len(_list) > 0:
            for e in _list:
                e()

    def doMouseRightKeyDown(self):
        _list = self.__Events[mouseRightKeyDown]
        if len(_list) > 0:
            for e in _list:
                e()

    def doMouseRightKeyClick(self):
        _list = self.__Events[mouseRightKeyClick]
        if len(_list) > 0:
            for e in _list:
                e()

    def doMouseMidKeyUp(self):
        _list = self.__Events[mouseMidKeyUp]
        if len(_list) > 0:
            for e in _list:
                e()

    def doMouseMidKeyDown(self):
        _list = self.__Events[mouseMidKeyDown]
        if len(_list) > 0:
            for e in _list:
                e()

    def doMouseMidKeyClick(self):
        _list = self.__Events[mouseMidKeyClick]
        if len(_list) > 0:
            for e in _list:
                e()

    def doDoubleClick(self):
        _list = self.__Events[mouseDoubleClick]
        if len(_list) > 0:
            for e in _list:
                e()

    def doKeyboardKeyUp(self, keyEnum):
        _list = self.__EventsKB[keyEnum + '0']
        if len(_list) > 0:
            for e in _list:
                e()

    def doKeyboardKeyDown(self, keyEnum):
        _list = self.__EventsKB[keyEnum + '1']
        if len(_list) > 0:
            for e in _list:
                e()

    def doKeyboardKeyDowning(self, keyEnum):
        _list = self.__EventsKB[keyEnum + '2']
        if len(_list) > 0:
            for e in _list:
                e()
