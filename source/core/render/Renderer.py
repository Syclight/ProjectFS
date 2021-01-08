class Renderer:
    def __init__(self, trans):
        self.__transform = trans
        self.__renderList = []

    def setTransform(self, trans):
        self.__transform = trans

    def getTransform(self):
        return self.__transform

    def add(self, *args):
        pass
