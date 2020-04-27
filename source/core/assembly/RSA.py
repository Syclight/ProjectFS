import rsa
import json

from rsa import PrivateKey


# 存储私钥，用getPrivateKeyFromPS读取
def outPrivateKeyToPS(path, privateKey) -> None:
    from source.util.ToolsFuc import IntToStr
    from source.const.Const import NUM_DICT_M
    _lis = [IntToStr(privateKey.n, NUM_DICT_M), IntToStr(privateKey.e, NUM_DICT_M), IntToStr(privateKey.d, NUM_DICT_M),
            IntToStr(privateKey.p, NUM_DICT_M), IntToStr(privateKey.q, NUM_DICT_M)]
    file = open(path, 'wb')
    byte = json.dumps(_lis).encode('utf-8')
    file.write(byte)
    file.close()


# 读取用outPrivateKeyToPS存储的私钥
def getPrivateKeyFromPS(path) -> PrivateKey:
    from source.util.ToolsFuc import StrToInt
    from source.const.Const import NUM_DICT_M
    file = open(path, 'rb')
    byte = file.read()
    file.close()
    pks = byte.decode('utf-8')
    pko = json.loads(pks)
    return PrivateKey(StrToInt(pko[0], NUM_DICT_M), StrToInt(pko[1], NUM_DICT_M), StrToInt(pko[2], NUM_DICT_M),
                      StrToInt(pko[3], NUM_DICT_M), StrToInt(pko[4], NUM_DICT_M))


# rsa加密
def rsaEncrypt(con, size) -> (str, PrivateKey):
    # 生成公钥、私钥
    (publicKey, privateKey) = rsa.newkeys(size)
    # 明文编码格式
    byte = con.encode('utf-8')
    # 公钥加密
    crypto = rsa.encrypt(byte, publicKey)
    return crypto, privateKey


# rsa解密
def rsaDecrypt(byte, privateKey) -> str:
    # 私钥解密
    con = rsa.decrypt(byte, privateKey)
    return con.decode('utf-8')
