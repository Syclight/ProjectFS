import pygame
import gc
from clazz.Const import SCENENUM_INIT


class gameApp:
    def __init__(self, appTitle, wight, height, isFullScreen, screenMod, colorBits):
        pygame.init()
        pygame.mixer.init()

        self.__Id = id(self)
        self.__appTitle = appTitle
        self.__screenWidth = wight
        self.__screenHeight = height
        self.__isFullScreen = isFullScreen
        self.__screenMod = screenMod
        self.__colorBits = colorBits

        from clazz.AppConfig import SceneMap
        if not SceneMap:
            raise Exception("'SceneMap' is Empty in AppConfig, 'SceneMap' mast have at least one element")
        self.__mapping = SceneMap
        self.__screen = pygame.display.set_mode((self.__screenWidth, self.__screenHeight), self.__screenMod,
                                                self.__colorBits)
        self.__scene = self.__mapping[SCENENUM_INIT][0](self.__screen)
        pygame.display.set_caption(self.__appTitle)

        self.isQuit = False
        print(appTitle + '\n-----控制台-----')

    def MainLoop(self):
        while not self.isQuit:
            self.__screen.fill((0, 0, 0))

            # 画屏幕
            self.__scene.draw()
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.quit()
                    pygame.quit()
                    self.isQuit = True
                elif event.type == pygame.MOUSEMOTION:
                    self.__scene.doMouseMotion(event.pos, event.rel, event.buttons)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.__scene.doMouseButtonDownEvent(event.pos, event.button)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.__scene.doMouseButtonUpEvent(event.pos, event.button)

            if self.__scene.isEnd:
                sceneNum = self.__scene.nextSceneNum
                nowScene = self.__mapping[sceneNum]
                del self.__scene
                gc.collect()
                if len(nowScene) > 1:
                    self.__scene = nowScene[0](self.__screen, nowScene[1:])
                else:
                    self.__scene = nowScene[0](self.__screen)
