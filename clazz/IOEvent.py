from enum import Enum

LEN_MOUSE_EVENT = 13
LEN_KB_EVENT = 0


class ioEvent3Enum(Enum):
    mouseIn = 0xA0000
    mouseOut = 0xA0001
    mouseLeftKeyUp = 0xA0002
    mouseLeftKeyDown = 0xA0003
    mouseLeftKeyClick = 0xA0004
    mouseRightKeyUp = 0xA0005
    mouseRightKeyDown = 0xA0006
    mouseRightKeyClick = 0xA0007
    mouseMidKeyUp = 0xA0008
    mouseMidKeyDown = 0xA0009
    mouseMidKeyClick = 0xA0010
    mouseDoubleClick = 0xA0012


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
        self.__Events = {0xA0000: [], 0xA0001: [], 0xA0002: [], 0xA0003: [], 0xA0004: [], 0xA0005: [], 0xA0006: [],
                         0xA0007: [], 0xA0008: [], 0xA0009: [], 0xA0010: [], 0xA0011: [], 0xA0012: []}
        self.__EventEnums = [ioEvent3Enum.mouseIn, ioEvent3Enum.mouseOut, ioEvent3Enum.mouseLeftKeyDown,
                             ioEvent3Enum.mouseLeftKeyUp, ioEvent3Enum.mouseLeftKeyClick,
                             ioEvent3Enum.mouseRightKeyDown,
                             ioEvent3Enum.mouseRightKeyUp, ioEvent3Enum.mouseRightKeyClick,
                             ioEvent3Enum.mouseMidKeyDown, ioEvent3Enum.mouseMidKeyUp, ioEvent3Enum.mouseMidKeyClick,
                             ioEvent3Enum.mouseDoubleClick]
        self.__KVMapping = {}

    def appendEvent(self, enum, fuc, ID) -> bool:
        if enum not in self.__EventEnums:
            return False
        _id = ID + hash(enum.name)

        if _id in self.__KVMapping.keys():
            return False
        self.__Events[enum.value].append(_id)
        self.__KVMapping[_id] = fuc
        return True

    def removeEvent(self, enum, ID) -> bool:
        if enum not in self.__EventEnums:
            return False
        _id = ID + hash(enum.name)

        idList = self.__Events[enum.value]
        if len(idList) < 1 or _id not in idList:
            return False

        self.__KVMapping.pop(_id)
        self.__Events[enum.value].remove(_id)
        return True

    def getSize(self):
        return len(self.__KVMapping)

    def doEvents(self, enum):
        if enum not in self.__EventEnums:
            return
        _list = self.__Events[enum.value]
        if len(_list) > 0:
            for e in _list:
                self.__KVMapping[e]()

    def doMouseIn(self):
        _list = self.__Events[0xA0000]
        if len(_list) > 0:
            for e in _list:
                self.__KVMapping[e]()

    def doMouseOut(self):
        _list = self.__Events[0xA0001]
        if len(_list) > 0:
            for e in _list:
                self.__KVMapping[e]()

    def doMouseLeftKeyUp(self):
        _list = self.__Events[0xA0002]
        if len(_list) > 0:
            for e in _list:
                self.__KVMapping[e]()

    def doMouseLeftKeyDown(self):
        _list = self.__Events[0xA0003]
        if len(_list) > 0:
            for e in _list:
                self.__KVMapping[e]()

    def doMouseLeftKeyClick(self):
        _list = self.__Events[0xA0004]
        if len(_list) > 0:
            for e in _list:
                self.__KVMapping[e]()

    def doMouseRightKeyUp(self):
        _list = self.__Events[0xA0005]
        if len(_list) > 0:
            for e in _list:
                self.__KVMapping[e]()

    def doMouseRightKeyDown(self):
        _list = self.__Events[0xA0006]
        if len(_list) > 0:
            for e in _list:
                self.__KVMapping[e]()

    def doMouseRightKeyClick(self):
        _list = self.__Events[0xA0007]
        if len(_list) > 0:
            for e in _list:
                self.__KVMapping[e]()

    def doMouseMidKeyUp(self):
        _list = self.__Events[0xA0008]
        if len(_list) > 0:
            for e in _list:
                self.__KVMapping[e]()

    def doMouseMidKeyDown(self):
        _list = self.__Events[0xA0009]
        if len(_list) > 0:
            for e in _list:
                self.__KVMapping[e]()

    def doMouseMidKeyClick(self):
        _list = self.__Events[0xA0010]
        if len(_list) > 0:
            for e in _list:
                self.__KVMapping[e]()

    def doDoubleClick(self):
        _list = self.__Events[0xA0011]
        if len(_list) > 0:
            for e in _list:
                self.__KVMapping[e]()

    def doKeyboardKeyUp(self, keyEnum):
        _list = self.__Events[keyEnum + 200]
        if len(_list) > 0:
            for e in _list:
                self.__KVMapping[e]()

    def doKeyboardKeyDown(self, keyEnum):
        _list = self.__Events[keyEnum + 201]
        if len(_list) > 0:
            for e in _list:
                self.__KVMapping[e]()

    def doKeyboardKeyDowning(self, keyEnum):
        _list = self.__Events[keyEnum + 202]
        if len(_list) > 0:
            for e in _list:
                self.__KVMapping[e]()
