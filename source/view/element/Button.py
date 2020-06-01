import pygame

from source.core.assembly.IOEvent import ioEvent3Enum
from source.core.const.Const import gl_Font_opt
from source.util.ToolsFuc import blankSurface
from source.view.baseClazz.Element import Element


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





