from source.core.math.Vector import vec4


class IntpolTypeEnum:
    line = 0
    cos = 1
    cubic = 2
    hermite = 3

    def __init__(self):
        self.param = list()


class AnimeFrame:
    def __init__(self, time=0, local=vec4()):
        self.time = time
        self.local = local

    def __str__(self):
        return "Anime::AnimeFrame<time: {}, local: {}>".format(self.time, self.local)

    def copy(self):
        return AnimeFrame(self.time, self.local)


class AnimePart:
    def __init__(self):
        self.__recordList = list()
        self.__index = -1

    def next(self):
        self.__index += 1
        if self.__index >= len(self.__recordList):
            self.__index = 0
        return self.__recordList[self.__index]

    def index(self):
        return self.__index

    def setData(self, animeFrame):
        self.__recordList.append(animeFrame)

    def setAllDatas(self, list):
        self.__recordList += list

    def getFrame(self, time, setPointer=False):
        for i in range(0, len(self.__recordList)):
            if self.__recordList[i].time == time:
                if setPointer:
                    self.__index = i
                return self.__recordList[i].copy()
        return

    def setPointer(self, index):
        self.__index = index


class Anime:
    def __init__(self):
        self.__recordList = list()
        self.__index = -1

    def next(self):
        self.__index += 1
        if self.__index >= len(self.__recordList):
            self.__index = 0
        return self.__recordList[self.__index]

    def index(self):
        return self.__index

    def setData(self, animePart):
        self.__recordList.append(animePart)

    def getPark(self, index, setPointer=False):
        if setPointer:
            self.__index = index
        return self.__recordList[index]

    def getFarme(self, time):
        for f in self.__recordList:
            frame = f.getFrame(time)
            if frame is not None:
                return frame
        return

    def setPointer(self, index):
        self.__index = index


# class AnimPlay:
#     def __init__(self, anim):
#         self.__anim = anim
#         self.__currentLocal = None
#
#     def timeLoop(self, time):
#         self.__anim.
#         self.__currentLocal = self.__anim.next()
#
#     def display(self, screen, index=-1):
#         if self.__currentLocal is not None:
#             if index == -1:


# class AnimFile:
#     pass
