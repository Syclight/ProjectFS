from source.const.Const import SCENENUM_INIT
from source.examples.ActorTest import ActorScene  # 物理场景测试
from source.examples.physicsTest import PhysicsScene
from source.examples.testSpriteScene import testSpriteScene  # 精灵场景测试
from source.view.baseClazz.Scene import Scene  # 空场景测试
from source.view.scene.Scenes import LogoScene  # 正常游戏运行流程入口

SceneMap = {SCENENUM_INIT: [ActorScene]}


def registerScene(sceneNum, sceneClass, paramList=None):
    if paramList is None:
        paramList = []
    vList = [sceneClass] + paramList
    SceneMap[sceneNum] = vList
