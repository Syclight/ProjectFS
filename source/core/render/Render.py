class Render:
    def __init__(self, surf):
        self.__renderList = list()
        self.__zIndexDict = dict()
        self.__surf = surf

    def __addZindex(self, key):
        if not key in self.__zIndexDict.keys():
            self.__zIndexDict[key] = 1
        else:
            self.__zIndexDict[key] += 1

    def add(self, e):
        self.__addZindex(e.zIndex)
        self.__renderList.append(e)


myDict = dict()
print(myDict[3])