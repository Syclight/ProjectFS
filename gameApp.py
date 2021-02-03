import os

import pygame
import gc

from source.core.assembly.Config import Config
from source.core.component.Console import Console
from source.core.component.Mixer import Mixer
from source.core.const.Const import SCENENUM_INIT
from source.util.ToolsFuc import getNotN


class gameApp:
    def __init__(self, appTitle, wight, height, isFullScreen, screenMod, colorBits):
        # 初始化要用到的库
        pygame.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.__mixer = Mixer()

        # 初始化App属性
        self.__Id = id(self)
        self.__appTitle = appTitle
        self.__screenWidth = wight
        self.__screenHeight = height
        self.__isFullScreen = isFullScreen
        self.__screenMod = screenMod
        self.__colorBits = colorBits
        self.__frameControl = False
        self.__fill = True

        from source.config.AppConfig import SceneMap
        if not SceneMap:
            raise Exception("'SceneMap' is Empty in AppConfig, 'SceneMap' mast have at least one element")
        self.__mapping = SceneMap

        pygame.display.set_caption(self.__appTitle)
        self.__screen = pygame.display.set_mode((self.__screenWidth, self.__screenHeight), self.__screenMod,
                                                self.__colorBits)
        self.__config = Config()
        self.__config.readConfig()
        self.__console = Console((0, 0, self.__screenWidth * 0.8, self.__screenHeight * 0.8))

        self.__clock = pygame.time.Clock()

        self.isQuit = False
        self.frameRate = self.__config.getFrameRate()
        if self.frameRate != 0:
            self.__frameControl = True

        self.__scene = self.__mapping[SCENENUM_INIT][0](self.__screen, self.__config, pygame.time.get_ticks(),
                                                        self.__mixer, self.__console)
        self.__scene.super_setup()

        if self.__scene.caption is not None:
            pygame.display.set_caption(self.__scene.caption)
            self.__appTitle = self.__scene.caption
        pygame.mouse.set_visible(self.__scene.mouseVisible)

        self.__console.log('achieved with Syclight\n' +
                           'inex recreation software 2020-2021 all rights reserved\n' + 'console version: ' +
                           self.__console.getVerStr() + '\n' +
                           self.__appTitle +
                           '\n------Console------\n')

    def MainLoop(self):
        while not self.isQuit:
            if self.__scene.mouseLimited:
                pygame.mouse.set_pos(self.__scene.mouseX, self.__scene.mouseY)
            if self.__frameControl:
                self.__clock.tick(self.frameRate)
            else:
                self.__clock.tick()
            self.__scene.FPS = round(self.__clock.get_fps(), 1)

            # 画屏幕
            self.__scene.super_draw()
            self.__scene.frameCount += 1
            self.__scene.super_doClockEvent(pygame.time.get_ticks())

            # 事件处理
            keyPressedList = getNotN(pygame.key.get_pressed(), 0)
            if keyPressedList:
                pygame.event.post(pygame.event.Event(25, {"keyPressedList": keyPressedList}))

            for event in pygame.event.get():
                if event.type == 12:  # QUIT
                    self.__mixer.quit()
                    pygame.quit()
                    self.isQuit = True
                    break
                elif event.type == 4:  # mouseMotion
                    self.__scene.super_doMouseMotion(event.rel, event.buttons)
                elif event.type == 5:  # mouseDown
                    self.__scene.mousePressed = True
                    self.__scene.super_doMouseButtonDownEvent(event.button)
                elif event.type == 6:  # mouseUp
                    self.__scene.mousePressed = False
                    self.__scene.super_doMouseButtonUpEvent(event.button)
                elif event.type == 2:
                    self.__scene.super_doKeyEvent(event.key, event.mod, 0, event.unicode)
                elif event.type == 3:
                    self.__scene.super_doKeyEvent(event.key, event.mod, 1)
                elif event.type == 25:
                    self.__scene.super_doKeyPressedEvent(event.keyPressedList)
                if 3 < event.type < 7:  # 与鼠标有关的事件
                    self.__scene.lastMousePos = self.__scene.mousePos
                    self.__scene.mousePos = event.pos
                    self.__scene.mouseX = self.__scene.mousePos[0]
                    self.__scene.mouseY = self.__scene.mousePos[1]

            if not self.isQuit:
                pygame.display.update()
                if self.__scene.isFill or self.__fill:
                    self.__screen.fill(self.__scene.fillColor)
                    self.__fill = False

            # 场景调度
            if self.__scene.isEnd:
                sceneNum = self.__scene.nextSceneNum
                nowScene = self.__mapping[sceneNum]
                del self.__scene
                gc.collect()
                if len(nowScene) > 1:
                    self.__scene = nowScene[0](self.__screen, self.__config, pygame.time.get_ticks(), self.__mixer,
                                               self.__console, nowScene[1:])
                else:
                    self.__scene = nowScene[0](self.__screen, self.__config, pygame.time.get_ticks(), self.__mixer,
                                               self.__console)
                self.__scene.super_setup()
                if self.__scene.resetMouse:
                    pygame.mouse.set_pos(self.__scene.mouseX, self.__scene.mouseY)
                pygame.mouse.set_visible(self.__scene.mouseVisible)
                if self.__scene.caption is not None:
                    self.__appTitle = self.__scene.caption
                    pygame.display.set_caption(self.__scene.caption)

    def getId(self):
        return self.__Id

# class gameApp:
#     def __init__(self, appTitle, wight, height, isFullScreen, screenMod, colorBits):
#         # 初始化要用到的库
#         pygame.init()
#         pygame.mixer.init()
#
#         # 初始化App属性
#         self.__Id = id(self)
#         self.__appTitle = appTitle
#         self.__screenWidth = wight
#         self.__screenHeight = height
#         self.__isFullScreen = isFullScreen
#         self.__screenMod = screenMod
#         self.__colorBits = colorBits
#         self.__frameControl = False
#         self.__fill = True
#
#         from source.config.AppConfig import SceneMap
#         if not SceneMap:
#             raise Exception("'SceneMap' is Empty in AppConfig, 'SceneMap' mast have at least one element")
#         self.__mapping = SceneMap
#
#         pygame.display.set_caption(appTitle)
#         self.__screen = pygame.display.set_mode((self.__screenWidth, self.__screenHeight), self.__screenMod,
#                                                 self.__colorBits)
#         self.__config = Config()
#         self.__config.readConfig()
#
#         self.__clock = pygame.time.Clock()
#
#         self.isQuit = False
#         self.frameRate = self.__config.getFrameRate()
#         if self.frameRate != 0:
#             self.__frameControl = True
#
#         print(appTitle + '\n-----控制台-----')
#
#         self.__scene = self.__mapping[SCENENUM_INIT][0](self.__screen, self.__config, pygame.time.get_ticks())
#
#         # 创建线程：
#         self.__optLoop = core_thread(1, "DrawLoop", 1, lambda: self.__optThread())
#         self.__drawLoop = core_thread(2, "DrawLoop", 2, lambda: self.__drawThread())
#         self.__msgLoop = core_thread(3, "MsgLoop", 3, lambda: self.__drawThread())
#         self.__sceneLoop = core_thread(4, 'SceneEstablish', 4, lambda: self.__sceneThread())
#
#     def MainLoop(self):
#         self.__optLoop.start()
#         self.__drawLoop.start()
#         self.__msgLoop.start()
#         self.__sceneLoop.start()
#         self.__optLoop.join()
#         self.__drawLoop.join()
#         self.__msgLoop.join()
#         self.__sceneLoop.join()
#
#     def __optThread(self):
#         while not self.isQuit:
#             if self.__frameControl:
#                 self.__clock.tick(self.frameRate)
#             else:
#                 self.__clock.tick()
#             self.__scene.FPS = round(self.__clock.get_fps(), 1)
#
#     def __drawThread(self):
#         while not self.isQuit:
#             if self.__scene.isFill or self.__fill:
#                 self.__screen.fill(self.__scene.fillColor)
#                 self.__fill = False
#
#             # 画屏幕
#             self.__scene.draw()
#             pygame.display.update()
#
#     def __msgThread(self):
#         while not self.isQuit:
#             self.__scene.doClockEvent(pygame.time.get_ticks())
#
#             keyPressedList = getNotN(pygame.key.get_pressed(), 0)
#             if keyPressedList:
#                 pygame.event.post(pygame.event.Event(25, {"keyPressedList": keyPressedList}))
#
#             for event in pygame.event.get():
#                 if event.type == 12:  # QUIT
#                     pygame.mixer.quit()
#                     pygame.quit()
#                     self.isQuit = True
#                     break
#                 elif event.type == 4:  # mouseMotion
#                     self.__scene.doMouseMotion(event.rel, event.buttons)
#                 elif event.type == 5:  # mouseDown
#                     self.__scene.doMouseButtonDownEvent(event.button)
#                 elif event.type == 6:  # mouseUp
#                     self.__scene.doMouseButtonUpEvent(event.button)
#                 elif event.type == 2:
#                     self.__scene.doKeyEvent(event.key, event.mod, 0, event.unicode)
#                 elif event.type == 3:
#                     self.__scene.doKeyEvent(event.key, event.mod, 1)
#                 elif event.type == 25:
#                     self.__scene.doKeyPressedEvent(event.keyPressedList)
#                 if 3 < event.type < 7:  # 与鼠标有关的事件
#                     self.__scene.lastMousePos = self.__scene.mousePos
#                     self.__scene.mousePos = event.pos
#                     self.__scene.mouseX = self.__scene.mousePos[0]
#                     self.__scene.mouseY = self.__scene.mousePos[1]
#
#     def __sceneThread(self):
#         while not self.isQuit:
#             if self.__scene.isEnd:
#                 sceneNum = self.__scene.nextSceneNum
#                 nowScene = self.__mapping[sceneNum]
#                 del self.__scene
#                 gc.collect()
#                 if len(nowScene) > 1:
#                     self.__scene = nowScene[0](self.__screen, self.__config, pygame.time.get_ticks(), nowScene[1:])
#                 else:
#                     self.__scene = nowScene[0](self.__screen, self.__config, pygame.time.get_ticks())
