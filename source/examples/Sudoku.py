import time
import pygame

from source.core.assembly.IOEvent import ioEvent3Enum
from source.core.const.Const import gl_Font_opt
from source.core.math.Shape import Rectangle
from source.util.ToolsFuc import blankSurface
from source.view.baseClazz.Scene import Scene
from source.view.element.Elements import ImgElement


class SudokuSprite(ImgElement):
    def __init__(self, area, path):
        super(SudokuSprite, self).__init__(area, path)
        self.__index = (0, 0)
        self.__shaderDistance = 10
        self.__mask = blankSurface((area.h, area.w), (40, 40, 40, 80))
        self.__val = 0
        self.__isStatic = False

        self.Events.appendEvent(ioEvent3Enum.mouseLeftKeyDown, lambda: self.__chaShader(True), 0)
        self.Events.appendEvent(ioEvent3Enum.mouseLeftKeyUp, lambda: self.__chaShader(False), 0)
        self.Events.appendEvent(ioEvent3Enum.mouseRightKeyDown, lambda: self.__clearVal(), 0)

    def __clearVal(self):
        if not self.__isStatic:
            self.__val = 0
            self.setImg(blankSurface(self.area.size()))

    def setIndex(self, index):
        self.__index = index

    def getIndex(self):
        return self.__index

    def setValue(self, val):
        self.__val = val

    def getValue(self):
        return self.__val

    def setIsStatic(self, isStatic):
        if self.__val != 0:
            self.__isStatic = isStatic

    def getIsStatic(self):
        return self.__isStatic

    def draw(self, screen):
        if not self.__isStatic:
            screen.blit(self.__mask, (self.area.x + self.__shaderDistance, self.area.y + self.__shaderDistance))
        super().draw(screen)

    def __chaShader(self, isDown):
        if isDown:
            self.zIndex -= 1
            self.area.x += 2
            self.area.y += 2
            self.__shaderDistance = 6
        else:
            self.zIndex += 1
            self.area.x -= 2
            self.area.y -= 2
            self.__shaderDistance = 10


class SudokuMap:
    def getName(self):
        pass

    def getSucScore(self):
        pass

    def getSize(self):
        pass

    def getSpriteSize(self):
        pass

    def getPuzzleList(self):
        pass

    def getAnswerList(self):
        pass

    def getInitSpritePosList(self):
        pass

    def buildSpriteMap(self):
        pass

    def getSpritePath(self, number):
        pass

    def getStaticSpritePath(self, number):
        pass

    def getBgSurface(self):
        pass

    def getPos(self, sprite):
        pass

    def getSprite(self, pos):
        pass

    def getSumOfInitEmpty(self):
        pass

    def playClickSound(self):
        pass

    def playBGM(self):
        pass


class SudokuMapLv0(SudokuMap):
    def __init__(self):
        self.__resImgPath = "F:\\Practice\\PyCharm\\PygameTest\\resource\\Test\\"
        self.__resImgName = "sudoku_"
        self.__resStaticImgName = "static_"
        self.__resImgExt = ".jpg"
        self.__resStaticImgExt = ".png"
        self.__resBgImg = "sudoku_bg_0.jpg"
        self.__resSoundPathClick = "F:\\Practice\\PyCharm\\PygameTest\\resource\\Wave\\Sound\\"
        self.__resSoundNameClick = "OPT_C.wav"
        self.__resMusicsPath = "F:\\Practice\\PyCharm\\PygameTest\\resource\\Test\\sudokuBGM\\"
        pygame.mixer.music.load(self.__resMusicsPath + "bgm0.mp3")

        self.__resSoundClick = pygame.mixer.Sound(self.__resSoundPathClick + self.__resSoundNameClick)

        self.__row = 0
        self.__col = 0
        self.__length = 60
        self.__index = 0
        self.__sumOfInitEmpty = 0

        self.__indexDict = dict()
        self.__elements = list()
        self.__data = {"puzzle": [0, 1, 0, 0, 0, 8, 4, 0, 7,
                                  9, 5, 0, 0, 0, 0, 0, 0, 0,
                                  0, 0, 8, 0, 1, 0, 0, 0, 0,
                                  0, 8, 2, 0, 0, 0, 0, 0, 0,
                                  7, 0, 0, 4, 0, 6, 0, 0, 8,
                                  0, 0, 0, 0, 0, 0, 6, 2, 0,
                                  0, 0, 0, 0, 5, 0, 7, 0, 0,
                                  0, 0, 0, 0, 0, 0, 0, 8, 2,
                                  5, 0, 3, 2, 0, 0, 0, 1, 6],
                       "answer": [2, 1, 6, 9, 3, 8, 4, 5, 7,
                                  9, 5, 4, 7, 6, 2, 8, 3, 1,
                                  3, 7, 8, 5, 1, 4, 2, 6, 9,
                                  6, 8, 2, 1, 9, 5, 3, 7, 4,
                                  7, 3, 5, 4, 2, 6, 1, 9, 8,
                                  4, 9, 1, 8, 7, 3, 6, 2, 5,
                                  8, 2, 9, 6, 5, 1, 7, 4, 3,
                                  1, 6, 7, 3, 4, 9, 5, 8, 2,
                                  5, 4, 3, 2, 8, 7, 9, 1, 6]}

        self.__initSpritePosList = list()

    def getName(self):
        return "1"

    def getSize(self):
        return self.__length * 9 + 2 * 6 + 4 * 2, self.__length * 9 + 2 * 6 + 4 * 2

    def getSucScore(self):
        return 81 - self.getSumOfInitEmpty()

    def getSpriteSize(self):
        return self.__length, self.__length

    def getPuzzleList(self):
        return self.__data["puzzle"]

    def getAnswerList(self):
        return self.__data["answer"]

    def getInitSpritePosList(self):
        length = len(self.__initSpritePosList)
        if length == 0:
            puzzleList = self.getPuzzleList()
            for i in range(0, len(puzzleList)):
                if puzzleList[i] != 0:
                    self.__initSpritePosList.append(i)
        return self.__initSpritePosList

    def buildSpriteMap(self):
        rowMarginStep, colMarginStep = 4, 4
        rowMargin, colMargin = rowMarginStep, colMarginStep
        while self.__col < 9:
            rowMarginStep = 8 if ((self.__row + 1) % 3 == 0) else 2
            colMarginStep = 8 if ((self.__col + 1) % 3 == 0) else 2

            ret = Rectangle(100 + (self.__row * self.__length + rowMargin),
                            10 + (self.__col * self.__length + colMargin),
                            self.__length, self.__length)
            number = self.__data["puzzle"][self.__index]
            self.__index += 1

            if number != 0:
                resName = self.__resImgPath + self.__resImgName + self.__resStaticImgName + str(number) + self.__resStaticImgExt
            else:
                resName = self.__resImgPath + self.__resImgName + "0" + self.__resImgExt
            element = SudokuSprite(ret, resName)
            self.__indexDict[element] = (self.__row, self.__col)
            element.setIndex((self.__row, self.__col))
            element.setValue(number)
            element.setIsStatic(True)
            element.Events.appendEvent(ioEvent3Enum.mouseLeftKeyDown, lambda: self.__resSoundClick.play(), 1)

            self.__elements.append(element)
            self.__row += 1
            rowMargin = rowMargin + rowMarginStep
            if self.__row == 9:
                self.__row = 0
                rowMargin = 4
                self.__col += 1
                colMargin = colMargin + colMarginStep

        return self.__elements

    def getSpritePath(self, number):
        return self.__resImgPath + self.__resImgName + str(number) + self.__resImgExt

    def getStaticSpritePath(self, number):
        return self.__resImgPath + self.__resImgName + self.__resStaticImgName + str(number) + self.__resStaticImgExt

    def getBgSurface(self):
        return pygame.image.load(self.__resImgPath + self.__resBgImg)

    def getPos(self, sprite):
        return self.__indexDict[sprite]

    def getSprite(self, pos):
        return self.__elements[pos[1] * 9 + pos[0]]

    def getSumOfInitEmpty(self):
        if self.__sumOfInitEmpty == 0:
            for i in self.__data:
                if i != 0:
                    self.__sumOfInitEmpty += 1
        return self.__sumOfInitEmpty

    def playClickSound(self):
        self.__resSoundClick.play()

    def playBGM(self):
        pygame.mixer.music.play(loops=-1)
        # pygame.mixer.music.queue(self.__resMusicsPath + "02.mp3")


class SudokuGame(Scene):
    def __init__(self, *args):
        super(SudokuGame, self).__init__(*args)
        self.__sudokuMap = SudokuMapLv0()
        self.__nowSelect = None
        self.__mask = None
        self.__score = 0
        self.__sucScore = 0
        self.__insertList = list()
        self.__allSprite = list()
        self.__isSuc = False

    def setup(self):
        self.bgSurface = self.__sudokuMap.getBgSurface()
        self.__sucScore = self.__sudokuMap.getSucScore()
        self.__insertList = self.__sudokuMap.getInitSpritePosList()
        self.__mask = blankSurface(self.__sudokuMap.getSpriteSize(), (40, 40, 40, 80))
        self.__allSprite = self.__sudokuMap.buildSpriteMap()

        self.createTextElement("Time:", color=(0, 0, 0), size=14)
        self.createTextElement("Level:" + self.__sudokuMap.getName(), color=(0, 0, 0), size=14, pos=self.TOP_RIGHT)
        self.caption = "Sududo Game 数独的游戏 v1.0.0  by 小叮铃制作组"

        self.render.open()
        self.render.add(self.__allSprite)
        self.render.close()
        # print(self.render,log())

        # self.__sudokuMap.playBGM()

    def draw(self):
        if not self.__isSuc and self.__nowSelect and self.__nowSelect.area.x > 0:
            self.screen.blit(self.__mask, (self.__nowSelect.area.x, self.__nowSelect.area.y))
        if self.__isSuc:
            self.createTextElement("成功！", pos=self.CENTER, color=(100, 104, 255), font=gl_Font_opt, size=60)

    def doClockEvent(self, NowClock):
        self.getCreatedElement(0).setText("Time:" + time.strftime("%H:%M:%S", time.localtime()))

    def doMouseButtonDownEvent(self, Button):
        if Button == 1:
            self.__nowSelect = self.focus

    def doKeyEvent(self, Key, Mod, Type, Unicode):
        inputCorrect = False
        if self.__nowSelect and self.__nowSelect.area.x > 0 and Type == 0:
            if self.__nowSelect.getIsStatic():
                return
            if Key == 127 or Key == 8:
                self.__nowSelect.setPath(self.__sudokuMap.getSpritePath(0))
                self.__nowSelect.setValue(0)
                inputCorrect = True
            elif 47 < Key < 58:
                self.__nowSelect.setPath(self.__sudokuMap.getSpritePath(Key - 48))
                self.__nowSelect.setValue(Key - 48)
                inputCorrect = True

            if inputCorrect:
                pos = self.__sudokuMap.getPos(self.__nowSelect)
                val = self.__nowSelect.getValue()
                if val == self.__sudokuMap.getAnswerList()[pos[1] * 9 + pos[0]]:
                    self.__nowSelect.setPath(self.__sudokuMap.getStaticSpritePath(val))
                    self.__nowSelect.setIsStatic(True)
                    self.__insertList.append(pos[1] * 9 + pos[0])
                    if len(self.__insertList) == len(self.__allSprite):
                        self.__isSuc = True



