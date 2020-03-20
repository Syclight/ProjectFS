from clazz.Const import SCENENUM_INIT
from clazz.Scene import LogoScene

SceneMap = {SCENENUM_INIT: [LogoScene]}


def registerScene(sceneNum, sceneClass, paramList=None):
    if paramList is None:
        paramList = []
    vList = [sceneClass] + paramList
    SceneMap[sceneNum] = vList
