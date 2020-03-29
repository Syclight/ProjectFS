from source.controller.assembly.IOEvent import IOEvent3, ElementHadDoEvent


class Element:
    def __init__(self, area, Events=None):
        self.area = area
        self.Events = Events
        if self.Events is None:
            self.Events = IOEvent3()
        self.EventsHadDo = ElementHadDoEvent()
        self.active = True
        self.zIndex = 0
        self.visual = True

    def draw(self, screen):
        pass
