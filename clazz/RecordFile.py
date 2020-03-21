from clazz.Const import RECORDFILE_PATH, RECORDFILE_USER, RSA_PK_FILE
from clazz.RSA import rsaEncrypt, rsaDecrypt, outPrivateKeyToPS, getPrivateKeyFromPS


class RecordFile:
    def __init__(self, path, fileName):
        self.__path = path
        self.__pf = path + fileName
        self.__file = None
        self.__Mapping = {}
        self.__check()

    def __check(self):
        try:
            f = open(self.__pf)
            f.close()
        except FileNotFoundError:
            print("File is not found.")

    def create(self, magMapping):
        content = ""
        for k, v in magMapping.items():
            content += k + '&' + v + '\n'
        crypto, privateKey = rsaEncrypt(content)
        outPrivateKeyToPS(self.__path + RSA_PK_FILE, privateKey)
        self.__file = open(self.__pf, 'wb')
        self.__file.write(crypto)
        self.__file.close()

    def getMapping(self):
        self.__file = open(self.__pf, 'rb')
        if not self.__Mapping:
            self.__Mapping.clear()

        content = self.__file.read()
        self.__file.close()
        content = rsaDecrypt(content, getPrivateKeyFromPS(self.__path + RSA_PK_FILE))

        lis = content.split('\n')
        lis.pop()
        for msg in lis:
            k, v = msg.split('&', 1)
            self.__Mapping[k] = v
        return self.__Mapping