"""
这是连接GameApp与Scene的主要媒介：

将要测试的场景类填入SceneMap = {SCENENUM_INIT: [XXX]}
的“XXX”处，运行程序即可

注意：\n
XXX处的场景类必须继承source.view.baseClazz.Scene中的Scene
如果想测试一些场景，在第一个场景类中注册下一个场景

例子：\n
from source.config.AppConfig import registerScene\n
registerScene(SCENENUM_TITLE, TitleScene)

SCENENUM_TITLE: int 场景号，上一个场景的nextSceneNum必须和与这个场景号一致，
两个场景才能连接起来
TitleScene： className 下一个场景的类名称

切记from...import...不能直接导入在代码头。例子中的两行必须写在一起。
"""
from source.core.const.Const import SCENENUM_INIT

from source.examples.ActorTest import ActorScene  # 物理场景测试
from source.examples.AstartTest import AstartTest  # A*寻路图形化演示
from source.examples.CanvasTest import canvasTest, water2d  # canvas测试与水纹模拟
from source.examples.RTS_Test import RobotRunScene  # Actor与A*结合测试场景
from source.examples.SpringSimulate import SpringSimulateScene, SpringMassSystemTestScene  # 弹簧模拟
from source.examples.Sudoku import SudokuGame  # 数独的游戏
from source.examples.TestPainter import TestPainterScene  # Painter测试
from source.examples.TestPick import pickTest  # pick测试
from source.examples.TextAreaTest import TextAreaTest  # textArea测试
from source.examples.noiseTest import noiseTestScene, noise1DScene  # 噪声测试
from source.examples.physicsTest import PhysicsScene, verletScene, verletSceneRotate  # 力学测试场景
from source.examples.reference import drawingBoard, createWave, sketchSphere, chain, paramEquation, \
    kaleidoscope, snowScene, MandelbrotSet, JuliaSet, IFS, LSystemScene, AnimatedCircle  # 范例
from source.examples.testSpriteScene import testSpriteScene, testAnimScene, trueAnimScene  # 精灵场景测试
from source.guitools.AnimaEditor import AnimaEditor  # GUITools 动画编辑器
from source.view.baseClazz.Scene import Scene  # 空场景
from source.view.origin.Scenes import OriginLogo, OriginTitle, OriginCGLogo  # 起源
from source.view.scene.Scenes import LogoScene  # 正常游戏运行流程入口

SceneMap = {SCENENUM_INIT: [OriginCGLogo]}


def registerScene(sceneNum, sceneClass, paramList=None):
    if paramList is None:
        paramList = []
    vList = [sceneClass] + paramList
    SceneMap[sceneNum] = vList
