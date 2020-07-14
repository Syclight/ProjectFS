import pygame

from source.core.assembly.IOEvent import ioEvent3Enum
from source.core.const.Const import gl_Font_opt, gl_Font
from source.core.dataType.CallBack import CallBack
from source.util.ToolsFuc import blankSurface, centeredYPos
from source.view.baseClazz.Element import Element
from source.view.element.Elements import TextElement


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
