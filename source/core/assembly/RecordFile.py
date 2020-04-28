from source.core.const.Const import RECORDFILE_HEAD, RSA_PK_FILE_EXN, RECORDFILE_SAVE_EXN
from source.core.assembly.RSA import rsaEncrypt, rsaDecrypt, outPrivateKeyToPS, getPrivateKeyFromPS


class NotRecordFileType(Exception):
    def __init__(self, arg):
        self.args = arg


class RecordFile:
    def __init__(self, path, fileName):
        self.__path = path
        self.__fileName = fileName
        self.__pf = path + fileName + RECORDFILE_SAVE_EXN
        self.__file = None
        self.__lis = []

    def create(self, lis):
        content = RECORDFILE_HEAD + '\n'
        for v in lis:
            content += v + '\n'
        crypto, privateKey = rsaEncrypt(content, 512)
        outPrivateKeyToPS(self.__path + self.__fileName + RSA_PK_FILE_EXN, privateKey)
        self.__file = open(self.__pf, 'wb')
        self.__file.write(crypto)
        self.__file.close()

    def getList(self):
        if not self.__lis:
            self.__lis.clear()

        self.__file = open(self.__pf, 'rb')
        content = self.__file.read()
        self.__file.close()
        content = rsaDecrypt(content, getPrivateKeyFromPS(self.__path + self.__fileName + RSA_PK_FILE_EXN))

        lis = content.split('\n')
        lis.pop()
        if lis[0] != RECORDFILE_HEAD:
            return None
        lis.remove(RECORDFILE_HEAD)
        for v in lis:
            self.__lis.append(v)
        return self.__lis
