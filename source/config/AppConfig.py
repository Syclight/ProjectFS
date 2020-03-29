from source.const.Const import SCENENUM_INIT
from source.examples.testSpriteScene import testSpriteScene
from source.view.baseClazz.Scene import Scene
from source.view.scene.Scenes import LogoScene

SceneMap = {SCENENUM_INIT: [LogoScene]}


def registerScene(sceneNum, sceneClass, paramList=None):
    if paramList is None:
        paramList = []
    vList = [sceneClass] + paramList
    SceneMap[sceneNum] = vList
