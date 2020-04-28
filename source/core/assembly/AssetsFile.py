class AssetsType:
    SUB = 0
    COM = 1
    EXP = 2


class fileChunk:
    def __init__(self, path, name, file, _type=None):
        self.path = path
        self.name = name
        self.file = file
        self.type = _type


class AssetsFile:
    """_path 所在目录"""

    def __init__(self, _path):
        self.__pa = _path
        self.__fs = []
        self.__fdct = {}
        self.__execute()

    def __readAll(self):
        import os
        files = os.listdir(self.__pa)
        _str = 'r'
        for fn in files:
            # f = open(os.path.join(self.__pa, fn), _str, encoding='utf-8')
            # flag = f.readline()
            # f.seek(0)
            fc = fileChunk(self.__pa, fn, open(os.path.join(self.__pa, fn), _str, encoding='utf-8'))
            self.__fs.append(fc)

    def __closeAll(self):
        for fc in self.__fs:
            fc.file.close()

    def __execute(self):
        self.__readAll()
        for fc in self.__fs:
            self.__fdct[fc.name] = fc.file.read()
            fc.file.close()

    # def __getFileByType(self, _type):
    #     _dict = {}
    #     for k, v in self.__fdct.items():
    #         if v.type == _type:
    #             _dict[k] = v
    #     return _dict

    def __decodeSUB(self, file_name):
        return self.__fdct[file_name].split('\n')

    def __decodeEXP(self, file_name):
        con = self.__fdct[file_name]
        con = con.replace('\\n', '\n')
        return con.split('^^')

    def decode(self, file_name, _type):
        if len(self.__fdct) < 1:
            return
        if _type == AssetsType.SUB:
            return self.__decodeSUB(file_name)
        elif _type == AssetsType.COM:
            pass
        elif _type == AssetsType.EXP:
            return self.__decodeEXP(file_name)
        return


# f = AssetsFile('F:/练习/PyCharm/PygameTest/data/assets/TitleScene')
# print(f.decode('T_P.assets'))
# print(f.decode('T_P_C.assets'))
# print(f.decode('I_T.assets', AssetsType.EXP))
