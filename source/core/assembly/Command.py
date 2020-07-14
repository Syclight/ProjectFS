class Comm:
    def __init__(self, name, fuc, *param):
        self.name = name
        self.callable = fuc
        self.param = param


class Command:
    def __init__(self):
        self.__comDict = dict()
        self.__MAXNUM = 125
        self.__curP = 0
        self.__sendCommList = list()
        self.__curStr = list()

    def registerCommand(self, c):
        if isinstance(Comm, c):
            self.__comDict[c.name] = c

    def sendComm(self, s):
        if s in self.__comDict.keys():
            self.__sendCommList.append(s)
            _comm = self.__comDict[s]
            _comm.callable(_comm.param)

    def inputComm(self, c):
        _length = len(self.__curStr)
        if _length < self.__MAXNUM:
            if _length == self.__curP:
                self.__curStr.append(c)
            else:
                self.__curStr.insert(self.__curP, c)
            self.__curP += 1

    # def __inputExc(self, c):
    #     if c=
