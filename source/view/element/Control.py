import time

import pygame

from source.core.assembly.IOEvent import ioEvent3Enum, getAsciiByIOEvent3Enum
from source.core.const.Const import gl_Font_opt, gl_Font
from source.core.math.MathUtil import mapping, signal
from source.util.KMP import KMPMatching
from source.util.ToolsFuc import blankSurface, centeredYPos
from source.view.baseClazz.Element import Element

# 空的Element
from source.view.element.Elements import TextElement


class BlankElement(Element):
    def __init__(self, area, color):
        t_Area = area
        if (isinstance(area, tuple) or isinstance(area, list)) and len(area) == 2:
            t_Area = (0, 0, area[0], area[1])
        super(BlankElement, self).__init__(t_Area)
        self.__col = color
        self.res_surface = None
        self.__build((self.area.w, self.area.h), self.__col)

    def __build(self, size, color):
        self.res_surface = blankSurface(size, color)

    def setSize(self, size):
        self.__build(size, self.__col)
        self.area.w = size[0]
        self.area.h = size[1]

    def setColor(self, color):
        self.__build((self.area.w, self.area.h), color)
        self.__col = color

    def setAlpha(self, val):
        self.res_surface.set_alpha(val)

    def draw(self, screen):
        screen.blit(self.res_surface, (self.area.x, self.area.y))


class Button(Element):
    def __init__(self, area, caption, size):
        super(Button, self).__init__(area)
        self.__caption = caption
        self.__textSize = size
        self.__size = self.area.size()
        self.__resShader = blankSurface(self.__size, (10, 10, 10, 200))
        self.__shaderRenderLocal = (self.area.x, self.area.y + 20)
        self.__resSuf = blankSurface(self.__size, (255, 255, 255))

        self.__build()

        self.Events.appendEvent(ioEvent3Enum.mouseLeftKeyDown, lambda: self.__evn_chShader(True), 0)
        self.Events.appendEvent(ioEvent3Enum.mouseLeftKeyUp, lambda: self.__evn_chShader(False), 0)

    def __build(self):
        # _shader = blankSurface(self.__size, (10, 10, 10, 200))
        _textTemp = pygame.font.Font(gl_Font_opt, self.__textSize)
        __textSuf = pygame.Surface((self.__textSize * len(self.__caption), self.__textSize))
        __textSuf.blit(_textTemp.render(self.__caption, 1, (0, 0, 0)), (10, 10))
        self.__resSuf.blit(__textSuf, (2, 2))

    def __evn_chShader(self, picked):
        if picked:
            self.__shaderRenderLocal = (self.__shaderRenderLocal[0], self.__shaderRenderLocal[1] - 10)
        else:
            self.__shaderRenderLocal = (self.__shaderRenderLocal[0], self.__shaderRenderLocal[1] + 10)

    def draw(self, screen):
        # screen.blit(self.__resShader, self.__shaderRenderLocal)
        screen.blit(self.__resSuf, (self.area.x, self.area.y))


class TextRender:
    def __init__(self, text, antialias=1, color=(0, 0, 0), bgColor=None):
        self.text = text
        self.antialias = antialias
        self.color = color
        self.bgColor = bgColor
        self.posX = 0
        self.posY = 0

    def createLineRender(self, text):
        pass


# 文本域
class TextArea(Element):
    ERROR_MSG = '<red>'
    HTML_TEAL = '</>'

    def __init__(self, area, padding_x=10, padding_y=10, font=gl_Font, fontSize=16, readonly=False,
                 bgColor=(0, 0, 0, 255), baseColor=(0, 0, 0, 255), fontColor=(-1, -1, -1, -1),
                 slidColor=(255, 255, 255, 100), slidWidth=10, autoLine=True, lineSpace=5,
                 textSpace=2):
        super(TextArea, self).__init__(area)
        self.__padding_x = padding_x
        self.__padding_y = padding_y
        self.__font = font
        self.__fontSize = fontSize
        self.__readonly = readonly
        self.__bgColor = bgColor
        self.__baseColor = baseColor
        self.__antiBgColor = (255 - self.__bgColor[0], 255 - self.__bgColor[1], 255 - self.__bgColor[2], 255)
        if fontColor == (-1, -1, -1, -1):
            self.__fontColor = self.__antiBgColor
        else:
            self.__fontColor = fontColor
        self.__slidColor = slidColor
        self.__slidWidth = slidWidth
        self.__autoLine = autoLine
        self.__lineSpace = lineSpace
        self.__textSpace = textSpace

        self.__verticalSlidLock = True
        self.__horizontalSlidLock = True
        self.__rollToTop = False
        self.__rollToBottom = False
        self.__allTextLength = 0
        self.__maxTextWidth = 0
        self.__text = ''
        self.__renderTextList = list()
        self.trueOneFontSize = self.__fontSize
        self.__offsetHeight = -1
        self.res_surface = None

        self.__areaBg = blankSurface((self.area.w, self.area.h), self.__bgColor)
        self.__slid = blankSurface((self.__slidWidth, self.area.h), self.__slidColor)
        self.__fontType = pygame.font.Font(self.__font, self.__fontSize)
        self.__areaBgPos = (0, 0)
        self.__curPtr = 0
        self.__lineList = list()
        self.__slidPosY = 0
        self.__nextTextPosX = self.__padding_x
        self.__nextTextPosY = self.__padding_y
        self.__interval = 0
        self.__showFlash = True

        self.Events.appendEvent(ioEvent3Enum.mouseRollDown, lambda: self.rollDown(True, self.trueOneFontSize), 1)
        self.Events.appendEvent(ioEvent3Enum.mouseRollUp, lambda: self.rollDown(False, self.trueOneFontSize), 1)
        self.Events.appendEvent(ioEvent3Enum.mouseLeftKeyDown, lambda: self.__mouKey(), 1)
        self.Events.appendEvent(ioEvent3Enum.mouseMotion, lambda: self.__dragSlidBar(), 1)
        self.Events.appendEvent(ioEvent3Enum.keyDown, self.keyInput, 1)
        self.Events.appendEvent(ioEvent3Enum.keyDowning, self.keyInput, 1)

        self.__buildSurface()

        self.__counter = 0

    def __mouKey(self):
        if (self.__slidPosY + self.__slid.get_rect().h > self.mousePos[1] > self.__slidPosY) and \
                (self.area.w > self.mousePos[0] > self.area.w - self.__slidWidth):
            return
        self.appendText('yes\n')

    # def __clickSlidChannel(self):
    #     if self.__verticalSlidLock:
    #         return
    #     if self.area.w > self.mousePos[0] > (self.area.w - self.__slidWidth):
    #         self.__areaBgPos = (
    #             self.__areaBgPos[0],
    #             int(mapping(self.mousePos[1], 0, self.area.h, 0, self.area.h - self.__allTextLength - self.__padding_y)))
    #         self.appendText('clicked Slid\n')

    def __dragSlidBar(self):
        if self.__verticalSlidLock:
            return
        if (self.__slidPosY + self.__slid.get_rect().h > self.mousePos[1] > self.__slidPosY) and \
                (self.area.w > self.mousePos[0] > self.area.w - self.__slidWidth):
            if self.mouseButtons == (1, 0, 0):
                shortH = self.mousePos[1] - self.__slidPosY
                print(shortH)

    def keyInput(self, key):
        _key = getAsciiByIOEvent3Enum(key)
        # 8 - 退格 
        # 9 - Tab 
        # 13 - 回车 
        # 16~18 - Shift, Ctrl, Alt 
        # 37~40 - 左上右下 
        # 35~36 - End Home 
        # 46 - Del 
        # 112~123 - F1 - F12 

        if _key == 8:
            _text = self.__text[:-1]
            self.__text = ''
            self.appendText(_text)
        elif _key == 13:
            self.appendText('\n')
        else:
            self.appendText(chr(_key))

    def __getSlidYByBgPos(self):
        return int(mapping(abs(self.__areaBgPos[1]), 0, self.__allTextLength, 0, self.area.h))

    def __getBgPosBySlidY(self):
        return self.__areaBgPos[0], int(mapping(self.__slidPosY, 0, self.area.h, 0, self.__allTextLength))

    def rollDown(self, isDown, step):
        if self.__verticalSlidLock:
            return
        # step += self.__padding_y
        if isDown and not self.__rollToBottom:
            self.__areaBgPos = (self.__areaBgPos[0], self.__areaBgPos[1] - step)
        if not isDown and not self.__rollToTop:
            self.__areaBgPos = (self.__areaBgPos[0], self.__areaBgPos[1] + step)
        self.__buildSurface()

    def __buildTextSurface(self):
        if not self.__text:
            return
        self.__nextTextPosY = self.__padding_y
        self.__nextTextPosX = self.__padding_x
        errorIndex = KMPMatching(self.__text, self.ERROR_MSG)
        for s in self.__text:
            renderText = TextRender(s, color=self.__fontColor)
            if renderText is not None:
                if renderText.text == '\n':
                    self.__nextTextPosY += self.trueOneFontSize + self.__lineSpace
                    self.__nextTextPosX = self.__padding_x
                    continue
                if renderText.text == '\r':
                    self.__nextTextPosX = self.__padding_x
                renderText.posY = self.__nextTextPosY
                renderText.posX = self.__nextTextPosX
                self.__areaBg.blit(
                    self.__fontType.render(renderText.text, renderText.antialias, renderText.color, renderText.bgColor),
                    (renderText.posX, renderText.posY))
                trueFontSize = self.__fontType.size(renderText.text)
                self.__renderTextList.append(renderText)
                self.__nextTextPosX += trueFontSize[0] + self.__textSpace

    def __buildSurface(self):
        self.res_surface = blankSurface((int(self.area.w), int(self.area.h)), self.__bgColor)
        if self.__offsetHeight >= 0:
            self.__areaBg = blankSurface((self.area.w, self.__allTextLength), self.__bgColor)
            if self.__verticalSlidLock:
                self.__verticalSlidLock = False
        else:
            self.__areaBg = blankSurface((self.area.w, self.area.h), self.__bgColor)
            if not self.__verticalSlidLock:
                self.__verticalSlidLock = True

        self.__buildTextSurface()

        if not self.__verticalSlidLock:
            slidHeight = (self.area.h / self.__allTextLength) * self.area.h
            self.__slid = blankSurface((self.__slidWidth, slidHeight), self.__slidColor)
            self.__slidPosY = self.__getSlidYByBgPos()
            if self.__areaBgPos[1] >= 0:
                self.__rollToTop = True
            else:
                self.__rollToTop = False
            if self.__allTextLength <= self.area.h + abs(self.__areaBgPos[1]):
                self.__rollToBottom = True
            else:
                self.__rollToBottom = False

    def appendText(self, text):
        text = str(text)
        self.__text += text
        self.__lineList = self.__text.split('\n')
        textLen = len(text.split('\n')) - 1

        if text:
            self.trueOneFontSize = self.__fontType.size(text[0])[1]
        else:
            self.trueOneFontSize = 0
        self.__allTextLength = self.__padding_y + len(self.__lineList) * (self.trueOneFontSize + self.__lineSpace)
        self.__offsetHeight = self.__allTextLength - self.area.h
        if self.__allTextLength - self.area.h > 0:
            self.rollDown(True, self.__padding_y + textLen * (self.trueOneFontSize + self.__lineSpace))
        self.__buildSurface()

    def insertText(self, pos, text):
        tempTextList = self.__text[:self.__getIndexByPos(pos)]
        _text = tempTextList[0] + text
        _text += tempTextList[1]
        self.__text = ''
        self.appendText(_text)

    def clearText(self):
        self.__text = ''
        self.__areaBgPos = (0, 0)
        self.__allTextLength = self.area.h
        self.__offsetHeight = self.__allTextLength - self.area.h
        self.appendText(self.__text)

    def appendLastLine(self, text):
        self.appendText(text)

    def getText(self):
        return self.__text

    def draw(self, screen):
        sec = time.clock()
        flashSurf = blankSurface((self.trueOneFontSize, self.trueOneFontSize), self.__bgColor)
        if sec - self.__interval >= 0.5:
            self.__showFlash = not self.__showFlash
            self.__interval = sec
        self.res_surface.fill(self.__bgColor)
        if self.__showFlash:
            flashSurf.blit(self.__fontType.render('|', 1, self.__antiBgColor), (0, 0))
        self.__areaBg.blit(flashSurf, (self.__nextTextPosX, self.__nextTextPosY))
        self.res_surface.blit(self.__areaBg, self.__areaBgPos)
        if not self.__verticalSlidLock:
            self.res_surface.blit(self.__slid, (self.area.w - self.__slidWidth, self.__slidPosY))
        screen.blit(self.res_surface, (self.area.x, self.area.y))


# 文字元素及其事件处理
class InputElement(Element):
    def __init__(self, area, text, padding=2, font=gl_Font, color=(255, 255, 255), bgColor=(0, 0, 0), antiAlias=1):
        super(InputElement, self).__init__(area)
        self.__font = font
        self.__text = text
        self.__padding = padding
        self.__color = color
        self.__bgColor = bgColor
        self.__antiAlias = antiAlias
        self.__buildSurface()

        self.Events.appendEvent(ioEvent3Enum.keyDown, self.__doKeyInput, 0)
        self.Events.appendEvent(ioEvent3Enum.keyDowning, self.__doKeyInput, 0)

    def __buildSurface(self):
        textSize = self.area.h - self.__padding * 2
        textTemp = pygame.font.Font(self.__font, textSize)
        self.res_surface = blankSurface(self.area.size(), (200, 200, 200))
        textSurface = textTemp.render(self.__text, self.__antiAlias, self.__color, self.__bgColor)
        self.res_surface.blit(textSurface, (0, centeredYPos(self.area.h, textSize)))

    def __doKeyInput(self, key):
        # 8 - 退格 
        # 9 - Tab 
        # 13 - 回车 
        # 16~18 - Shift, Ctrl, Alt 
        # 37~40 - 左上右下 
        # 35~36 - End Home 
        # 46 - Del 
        # 112~123 - F1 - F12 

        if key == 8:
            self.setText(self.__text[:-1])
        # elif key in (9, 13, 16, 17, 18):
        #     return
        # elif 36 < key < 41 or 34 < key < 37 or 111 < key < 124:
        #     return
        else:
            self.setText(self.__text + chr(key))

    def draw(self, screen):
        screen.blit(self.res_surface, (self.area.x, self.area.y))

    def setBackgroundColor(self, bgColor):
        self.__bgColor = bgColor
        self.__buildSurface()

    def setPadding(self, padding):
        self.__padding = padding
        self.__buildSurface()

    def setText(self, text):
        self.__text = str(text)
        self.__buildSurface()

    def setFont(self, font):
        self.__font = font
        self.__buildSurface()

    def setSize(self, size):
        self.area.h = size + self.__padding
        self.__buildSurface()

    def setColor(self, color):
        self.__color = color
        self.__buildSurface()
