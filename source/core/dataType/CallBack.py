class CallBack:
    def __init__(self, name, param):
        self.__fucName = name
        self.__param = param

    def exc(self):
        self.__fucName(self.__param)

