from xml.dom.minidom import parse
import xml.dom.minidom

from source.const.Const import DATATYPE_STR_BOOL, DATATYPE_STR_INT, DATATYPE_STR_STR, DATATYPE_STR_COMPLEX, \
    DATATYPE_STR_FLOAT


class SceneNotException(Exception):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return str("Scene Class \'" + self.name + "\' not found")


class XMLOperator:
    def __init__(self, path):
        self.__path = path
        self.__DOMTree = xml.dom.minidom.parse(self.__path)
        self.__collection = self.__DOMTree.documentElement


def ret_init_global_sceneList(path) -> list:
    _lis = []
    DOMTree = xml.dom.minidom.parse(path)
    collection = DOMTree.documentElement
    path_collection = collection.getElementsByTagName('baseclass-path')
    paths = path_collection[0].getElementsByTagName('path')
    for p in paths:
        if p.getAttribute('type') == 'scene':
            _lis.append((p.getAttribute('value')))
    path_collection = collection.getElementsByTagName('subclass-path')
    paths = path_collection[0].getElementsByTagName('path')
    for p in paths:
        if p.getAttribute('type') == 'scene':
            _lis.append((p.getAttribute('value')))
    return _lis


def loadSceneFormConfig(sceneNum):
    str_sceneNum = str(sceneNum)
    DOMTree = xml.dom.minidom.parse("F:/练习/PyCharm/PygameTest/framework-config/app-config.xml")
    collection = DOMTree.documentElement
    registeredScene_collection = collection.getElementsByTagName('registered-scene')
    rgs = registeredScene_collection[0].getElementsByTagName('scene')
    class_str = ''
    param_list = []
    for s in rgs:
        if s.getAttribute('scene-num') == str_sceneNum:
            class_str = s.getAttribute('class-string')
            params = s.getElementsByTagName('param')
            for p in params:
                _type = p.getAttribute('type')
                _val = p.childNodes[0].data
                if _type == DATATYPE_STR_BOOL or _type == DATATYPE_STR_INT:
                    param_list.append(int(_val))
                elif _type == DATATYPE_STR_FLOAT:
                    param_list.append(float(_val))
                elif _type == DATATYPE_STR_STR:
                    param_list.append(_val)
                elif _type == DATATYPE_STR_COMPLEX:
                    param_list.append(complex(_val))
            break
    return class_str, param_list
