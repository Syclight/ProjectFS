from clazz.Const import SCREEN_INIT
from clazz.Scene import LogoScene

SceneMap = {SCREEN_INIT: [LogoScene]}


def registerScene(sceneNum, sceneClass, paramList=None):
    if paramList is None:
        paramList = []
    vList = [sceneClass] + paramList
    SceneMap[sceneNum] = vList
