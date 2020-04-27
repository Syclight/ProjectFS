LEN_MOUSE_EVENT = 13
LEN_KB_EVENT = 0


class ioEvent3Enum:
    # 鼠标
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
    mouseMidKeyClick = 0xA000A
    mouseDoubleClick = 0xA000B
    mouseMotion = 0xA000C
    mouseRollUp = 0xA000D
    mouseRollDown = 0xA000E

    # 键盘
    keyDown = 0xB1000
    keyDowning = 0xB2000
    keyUp = 0xB3000
    key_A = 0xC0000
    key_B = 0xC0001
    key_C = 0xC0002
    key_D = 0xC0003
    key_E = 0xC0004
    key_F = 0xC0005
    key_G = 0xC0006
    key_H = 0xC0007
    key_I = 0xC0008
    key_J = 0xC0009
    key_K = 0xC000A
    key_L = 0xC000B
    key_M = 0xC000C
    key_N = 0xC000D
    key_O = 0xC000E
    key_P = 0xC000F
    key_Q = 0xC0010
    key_R = 0xC0011
    key_S = 0xC0012
    key_T = 0xC0013
    key_U = 0xC0014
    key_V = 0xC0015
    key_W = 0xC0016
    key_X = 0xC0017
    key_Y = 0xC0018
    key_Z = 0xC0019
    key_0 = 0xC001A
    key_1 = 0xC001B
    key_2 = 0xC001C
    key_3 = 0xC001D
    key_4 = 0xC001E
    key_5 = 0xC001F
    key_6 = 0xC0020
    key_7 = 0xC0021
    key_8 = 0xC0022
    key_9 = 0xC0023
    key_F1 = 0xC0025
    key_F2 = 0xC0026
    key_F3 = 0xC0027
    key_F4 = 0xC0028
    key_F5 = 0xC0029
    key_F6 = 0xC002A
    key_F7 = 0xC002B
    key_F8 = 0xC002C
    key_F9 = 0xC002D
    key_F10 = 0xC002E
    key_F11 = 0xC002F
    key_F12 = 0xC0030
    key_Tab = 0xC0031
    key_CapsLock = 0xC0032
    key_Shift = 0xC0033
    key_Ctrl = 0xC0034
    key_Alt = 0xC0035
    key_Space = 0xC0036
    key_Enter = 0xC0037
    key_Backspace = 0xC0038
    key_Esc = 0xC0039
    key_Delete = 0xC003A
    key_Insert = 0xC003B
    key_Up = 0xC003C
    key_Down = 0xC003D
    key_Left = 0xC003E
    key_Right = 0xC003F
    key_Sym33 = 0xC0061
    key_Sym34 = 0xC0062
    key_Sym35 = 0xC0063
    key_Sym36 = 0xC0064
    key_Sym37 = 0xC0065
    key_Sym38 = 0xC0066
    key_Sym39 = 0xC0067
    key_Sym40 = 0xC0068
    key_Sym41 = 0xC0069
    key_Sym42 = 0xC006A
    key_Sym43 = 0xC006B
    key_Sym44 = 0xC006C
    key_Sym45 = 0xC006D
    key_Sym46 = 0xC006E
    key_Sym47 = 0xC006F


# Element处理处理Io事件列表
class ElementHadDoEvent:
    def __init__(self):
        self.Key = None
        self.hadDoMouseIn = False
        self.hadDoMouseOut = True
        self.hadDoMouseLeftKeyUp = True
        self.hadDoMouseLeftKeyDown = False
        self.hadDoMouseLeftKeyClick = False
        self.hadDoMouseRightKeyUp = True
        self.hadDoMouseRightKeyDown = False
        self.hadDoMouseRightKeyClick = False
        self.hadDoMouseMidKeyUp = False
        self.hadDoMouseMidKeyDown = False
        self.hadDoMouseMidKeyClick = False
        self.hadDoDoubleClick = False
        self.hadDoKeyboardKeyUp = False
        self.hadDoKeyboardKeyDown = False
        self.hadDoKeyboardKeyDowning = False


class IOEvent:
    def doMouseMotion(self):
        pass

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

    def doMouseMotion(self):
        pass

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
                         0xA0007: [], 0xA0008: [], 0xA0009: [], 0xA000A: [], 0xA000B: [], 0xA000C: [], 0xA000D: [],
                         0xA000E: [],
                         0xF1000: [], 0xF2000: [], 0xF3000: [], 0xF1001: [], 0xF2001: [], 0xF3001: [], 0xF1002: [],
                         0xF2002: [], 0xF3002: [], 0xF1003: [], 0xF2003: [], 0xF3003: [], 0xF1004: [], 0xF2004: [],
                         0xF3004: [], 0xF1005: [], 0xF2005: [], 0xF3005: [], 0xF1006: [], 0xF2006: [], 0xF3006: [],
                         0xF1007: [], 0xF2007: [], 0xF3007: [], 0xF1008: [], 0xF2008: [], 0xF3008: [], 0xF1009: [],
                         0xF2009: [], 0xF3009: [], 0xF100A: [], 0xF200A: [], 0xF300A: [], 0xF100B: [], 0xF200B: [],
                         0xF300B: [], 0xF100C: [], 0xF200C: [], 0xF300C: [], 0xF100D: [], 0xF200D: [], 0xF300D: [],
                         0xF100E: [], 0xF200E: [], 0xF300E: [], 0xF100F: [], 0xF200F: [], 0xF300F: [], 0xF1010: [],
                         0xF2010: [], 0xF3010: [], 0xF1011: [], 0xF2011: [], 0xF3011: [], 0xF1012: [], 0xF2012: [],
                         0xF3012: [], 0xF1013: [], 0xF2013: [], 0xF3013: [], 0xF1014: [], 0xF2014: [], 0xF3014: [],
                         0xF1015: [], 0xF2015: [], 0xF3015: [], 0xF1016: [], 0xF2016: [], 0xF3016: [], 0xF1017: [],
                         0xF2017: [], 0xF3017: [], 0xF1018: [], 0xF2018: [], 0xF3018: [], 0xF1019: [], 0xF2019: [],
                         0xF3019: [], 0xF101A: [], 0xF201A: [], 0xF301A: [], 0xF101B: [], 0xF201B: [], 0xF301B: [],
                         0xF101C: [], 0xF201C: [], 0xF301C: [], 0xF101D: [], 0xF201D: [], 0xF301D: [], 0xF101E: [],
                         0xF201E: [], 0xF301E: [], 0xF101F: [], 0xF201F: [], 0xF301F: [], 0xF1020: [], 0xF2020: [],
                         0xF3020: [], 0xF1021: [], 0xF2021: [], 0xF3021: [], 0xF1022: [], 0xF2022: [], 0xF3022: [],
                         0xF1023: [], 0xF2023: [], 0xF3023: [], 0xF1024: [], 0xF2024: [], 0xF3024: [], 0xF1025: [],
                         0xF2025: [], 0xF3025: [], 0xF1026: [], 0xF2026: [], 0xF3026: [], 0xF1027: [], 0xF2027: [],
                         0xF3027: [], 0xF1028: [], 0xF2028: [], 0xF3028: [], 0xF1029: [], 0xF2029: [], 0xF3029: [],
                         0xF102A: [], 0xF202A: [], 0xF302A: [], 0xF102B: [], 0xF202B: [], 0xF302B: [], 0xF102C: [],
                         0xF202C: [], 0xF302C: [], 0xF102D: [], 0xF202D: [], 0xF302D: [], 0xF102E: [], 0xF202E: [],
                         0xF302E: [], 0xF102F: [], 0xF202F: [], 0xF302F: [], 0xF1030: [], 0xF2030: [], 0xF3030: [],
                         0xF1031: [], 0xF2031: [], 0xF3031: [], 0xF1032: [], 0xF2032: [], 0xF3032: [], 0xF1033: [],
                         0xF2033: [], 0xF3033: [], 0xF1034: [], 0xF2034: [], 0xF3034: [], 0xF1035: [], 0xF2035: [],
                         0xF3035: [], 0xF1036: [], 0xF2036: [], 0xF3036: [], 0xF1037: [], 0xF2037: [], 0xF3037: [],
                         0xF1038: [], 0xF2038: [], 0xF3038: [], 0xF1039: [], 0xF2039: [], 0xF3039: [], 0xF103A: [],
                         0xF203A: [], 0xF303A: [], 0xF103B: [], 0xF203B: [], 0xF303B: [], 0xF103C: [], 0xF203C: [],
                         0xF303C: [], 0xF103D: [], 0xF203D: [], 0xF303D: [], 0xF103E: [], 0xF203E: [], 0xF303E: [],
                         0xF103F: [], 0xF203F: [], 0xF303F: [], 0xF1040: [], 0xF2040: [], 0xF3040: [], 0xF1041: [],
                         0xF2041: [], 0xF3041: [], 0xF1042: [], 0xF2042: [], 0xF3042: [], 0xF1043: [], 0xF2043: [],
                         0xF3043: [], 0xF1044: [], 0xF2044: [], 0xF3044: [], 0xF1045: [], 0xF2045: [], 0xF3045: [],
                         0xF1046: [], 0xF2046: [], 0xF3046: [], 0xF1047: [], 0xF2047: [], 0xF3047: [], 0xF1048: [],
                         0xF2048: [], 0xF3048: [], 0xF1049: [], 0xF2049: [], 0xF3049: [], 0xF104A: [], 0xF204A: [],
                         0xF304A: [], 0xF104B: [], 0xF204B: [], 0xF304B: [], 0xF104C: [], 0xF204C: [], 0xF304C: [],
                         0xF104D: [], 0xF204D: [], 0xF304D: [], 0xF104E: [], 0xF204E: [], 0xF304E: [], 0xF104F: [],
                         0xF204F: [], 0xF304F: [], 0xF1050: [], 0xF2050: [], 0xF3050: [], 0xF1051: [], 0xF2051: [],
                         0xF3051: [], 0xF1052: [], 0xF2052: [], 0xF3052: [], 0xF1053: [], 0xF2053: [], 0xF3053: [],
                         0xF1054: [], 0xF2054: [], 0xF3054: [], 0xF1055: [], 0xF2055: [], 0xF3055: [], 0xF1056: [],
                         0xF2056: [], 0xF3056: [], 0xF1057: [], 0xF2057: [], 0xF3057: [], 0xF1058: [], 0xF2058: [],
                         0xF3058: [], 0xF1059: [], 0xF2059: [], 0xF3059: [], 0xF105A: [], 0xF205A: [], 0xF305A: [],
                         0xF105B: [], 0xF205B: [], 0xF305B: [], 0xF105C: [], 0xF205C: [], 0xF305C: [], 0xF105D: [],
                         0xF205D: [], 0xF305D: [], 0xF105E: [], 0xF205E: [], 0xF305E: [], 0xF105F: [], 0xF205F: [],
                         0xF305F: [], 0xF1060: [], 0xF2060: [], 0xF3060: [], 0xF1061: [], 0xF2061: [], 0xF3061: [],
                         0xF1062: [], 0xF2062: [], 0xF3062: [], 0xF1063: [], 0xF2063: [], 0xF3063: [], 0xF1064: [],
                         0xF2064: [], 0xF3064: [], 0xF1065: [], 0xF2065: [], 0xF3065: [], 0xF1066: [], 0xF2066: [],
                         0xF3066: [], 0xF1067: [], 0xF2067: [], 0xF3067: [], 0xF1068: [], 0xF2068: [], 0xF3068: [],
                         0xF1069: [], 0xF2069: [], 0xF3069: [], 0xF106A: [], 0xF206A: [], 0xF306A: [], 0xF106B: [],
                         0xF206B: [], 0xF306B: [], 0xF106C: [], 0xF206C: [], 0xF306C: [], 0xF106D: [], 0xF206D: [],
                         0xF306D: [], 0xF106E: [], 0xF206E: [], 0xF306E: [], 0xF106F: [], 0xF206F: [], 0xF306F: []}
        self.__KVMapping = {}

    def appendEvent(self, enumValue, fuc, ID) -> bool:
        if enumValue not in self.__Events.keys():
            return False
        _id = (ID << 6) + enumValue
        if _id in self.__KVMapping.keys():
            return False
        self.__Events[enumValue].append(_id)
        self.__KVMapping[_id] = fuc
        return True

    def removeEvent(self, enumValue, ID) -> bool:
        _id = (ID << 6) + enumValue
        if enumValue not in self.__Events.keys():
            return False

        _list = self.__Events[enumValue]
        if len(_list) < 1 or _id not in _list:
            return False

        self.__KVMapping.pop(_id)
        self.__Events[enumValue].remove(_id)
        return True

    def getSize(self):
        return len(self.__KVMapping)

    def doEvents(self, enumValue):
        _key = enumValue
        if _key not in self.__Events.keys():
            return
        for e in self.__Events[_key]:
            self.__KVMapping[e]()

    def doMouseIn(self):
        for e in self.__Events[0xA0000]:
            self.__KVMapping[e]()

    def doMouseOut(self):
        for e in self.__Events[0xA0001]:
            self.__KVMapping[e]()

    def doMouseLeftKeyUp(self):
        for e in self.__Events[0xA0002]:
            self.__KVMapping[e]()

    def doMouseLeftKeyDown(self):
        for e in self.__Events[0xA0003]:
            self.__KVMapping[e]()

    def doMouseLeftKeyClick(self):
        for e in self.__Events[0xA0004]:
            self.__KVMapping[e]()

    def doMouseRightKeyUp(self):
        for e in self.__Events[0xA0005]:
            self.__KVMapping[e]()

    def doMouseRightKeyDown(self):
        for e in self.__Events[0xA0006]:
            self.__KVMapping[e]()

    def doMouseRightKeyClick(self):
        for e in self.__Events[0xA0007]:
            self.__KVMapping[e]()

    def doMouseMidKeyUp(self):
        for e in self.__Events[0xA0008]:
            self.__KVMapping[e]()

    def doMouseMidKeyDown(self):
        for e in self.__Events[0xA0009]:
            self.__KVMapping[e]()

    def doMouseMidKeyClick(self):
        for e in self.__Events[0xA000A]:
            self.__KVMapping[e]()

    def doDoubleClick(self):
        for e in self.__Events[0xA000B]:
            self.__KVMapping[e]()

    def doMouseMotion(self):
        for e in self.__Events[0xA000C]:
            self.__KVMapping[e]()

    def doMouserRollUp(self):
        for e in self.__Events[0xA000D]:
            self.__KVMapping[e]()

    def doMouserRollDown(self):
        for e in self.__Events[0xA000E]:
            self.__KVMapping[e]()

    def doKeyboardKeyUp(self, keyEnum):
        _key = keyEnum | ioEvent3Enum.keyUp
        if _key not in self.__Events.keys():
            return
        for e in self.__Events[_key]:
            self.__KVMapping[e]()

    def doKeyboardKeyDown(self, keyEnum):
        _key = keyEnum | ioEvent3Enum.keyDown
        if _key not in self.__Events.keys():
            return
        for e in self.__Events[_key]:
            self.__KVMapping[e]()

    def doKeyboardKeyDowning(self, keyEnum):
        _key = keyEnum | ioEvent3Enum.keyDowning
        if _key not in self.__Events.keys():
            return
        for e in self.__Events[_key]:
            self.__KVMapping[e]()
