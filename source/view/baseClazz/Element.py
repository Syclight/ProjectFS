from source.core.assembly.IOEvent import IOEvent3, ElementHadDoEvent
from source.core.math.Shape import Shape
from source.core.math.Shape import Rectangle


class Element:
    def __init__(self, area, msgQueue=None, Events=None):
        _area = None
        if isinstance(area, Shape):
            _area = area
        else:
            _area = Rectangle(area[0], area[1], area[2], area[3])
        self.area = _area
        self.msgQueue = msgQueue
        self.Events = Events
        if self.Events is None:
            self.Events = IOEvent3()
        self.EventsHadDo = ElementHadDoEvent()
        self.active = True
        self.zIndex = 0
        self.visual = True
        self.mouseLastPos = (0, 0)
        self.mousePos = (0, 0)
        self.mouseButtons = (0, 0, 0)
        self.mouseRel = (0, 0)

    def recoverEvent(self):
        # self.hadDoMouseIn = False
        # self.hadDoMouseOut = True
        # self.hadDoMouseLeftKeyUp = True
        # self.hadDoMouseLeftKeyDown = False
        # self.hadDoMouseLeftKeyClick = False
        # self.hadDoMouseRightKeyUp = False
        # self.hadDoMouseRightKeyDown = False
        # self.hadDoMouseRightKeyClick = False
        # self.hadDoMouseMidKeyUp = False
        # self.hadDoMouseMidKeyDown = False
        # self.hadDoMouseMidKeyClick = False
        # self.hadDoDoubleClick = False
        # self.hadDoKeyboardKeyUp = False
        # self.hadDoKeyboardKeyDown = False
        # self.hadDoKeyboardKeyDowning = False
        self.EventsHadDo = ElementHadDoEvent()

    def draw(self, screen):
        pass
