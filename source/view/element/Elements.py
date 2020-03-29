from source.view.baseClazz.Element import Element
from source.controller.assembly.IOEvent import *
from source.const.Const import *
from source.util.ToolsFuc import *


# 消息框Elements
class MessageBox(Element):
    def __init__(self, bgWidth, bgHeight, text):
        super(MessageBox, self).__init__(pygame.Rect(centeredXPos(bgWidth, 180, 0), centeredXPos(bgHeight, 100, 0), 180, 100))
        self.__Text = text
        self.__buildSurface()

    def __buildSurface(self):
        self.__E_bg = blankSurface((180, 100), (255, 255, 255, 100))
        concernWidth = len(self.__Text) * 18
        self.__E_Text = TextElement(
            pygame.Rect(centeredXPos(180, concernWidth, self.area.left), centeredYPos(100, 18, self.area.top),
                        concernWidth, 20), self.__Text, gl_Font_opt, 18, (0, 0, 0), True)
        self.__E_okButt = TextElement(pygame.Rect(self.area.left + 40, self.area.top + 70, 36, 18), '确定', gl_Font_opt,
                                      16, (0, 0, 0), True)
        self.__E_cancelButt = TextElement(pygame.Rect(self.area.left + 80, self.area.top + 70, 36, 18), '取消',
                                          gl_Font_opt, 16, (0, 0, 0), True)

    def draw(self, screen):
        screen.blit(self.__E_bg, (self.area.left, self.area.top))
        screen.blit(self.__E_Text.res_surface, (self.__E_Text.area.left, self.__E_Text.area.top))
        screen.blit(self.__E_okButt.res_surface, (self.__E_okButt.area.left, self.__E_okButt.area.top))
        screen.blit(self.__E_cancelButt.res_surface, (self.__E_cancelButt.area.left, self.__E_cancelButt.area.top))


# 标题页面固定元素
class TitleConstElement(Element):
    def __init__(self, area, res_Surface):
        super(TitleConstElement, self).__init__(area, IOEvent())
        self.res_surface = res_Surface

    def setAlpha(self, alpha):
        self.res_surface.set_alpha(alpha)

    def draw(self, screen):
        screen.blit(self.res_surface, (self.area.left, self.area.top))


# -----标题页面可交互元素及事件处理---开始-----

# 鼠标左键按下鼠标改变元素位置事件
def changeAraPos(e):
    e.area.top += 1
    e.area.left += 1


# 鼠标左键放开鼠标移出还原元素位置事件
def backAraPos(e):
    e.area.top -= 1
    e.area.left -= 1


# 鼠标移入改变样式
def changeStyle(e):
    e.setClipRect(pygame.Rect(e.ClipRect.left + 30, e.ClipRect.top, e.ClipRect.width, e.ClipRect.height))


# 鼠标移出改变样式
def backStyle(e):
    e.setClipRect(pygame.Rect(e.ClipRect.left - 30, e.ClipRect.top, e.ClipRect.width, e.ClipRect.height))


# 标题页面选项元素
class TitleOptElement(Element):
    def __init__(self, area, res_img, clipRect, colorKey):
        super(TitleOptElement, self).__init__(area, IOEvent2())
        self.res_Img = res_img
        self.ClipRect = clipRect
        self.ColorKey = colorKey
        self.__buildSurface()

        self.Events.mouseIn.append(lambda: changeStyle(self))
        self.Events.mouseOut.append(lambda: backStyle(self))
        self.Events.mouseLeftKeyDown.append(lambda: changeAraPos(self))
        self.Events.mouseLeftKeyUp.append(lambda: backAraPos(self))

    def __buildSurface(self):
        self.res_surface = pygame.Surface((self.ClipRect.width, self.ClipRect.height)).convert()
        self.res_surface.set_colorkey(self.ColorKey)
        self.res_surface.blit(self.res_Img, (-self.ClipRect.top, -self.ClipRect.left))

    def draw(self, screen):
        screen.blit(self.res_surface, (self.area.left, self.area.top))

    def setResImg(self, res_Img):
        self.res_Img = res_Img
        self.__buildSurface()

    def setClipRect(self, clipRect):
        self.ClipRect = clipRect
        self.__buildSurface()

    def setColorKey(self, colorKey):
        self.ColorKey = colorKey
        self.__buildSurface()

    def setAlpha(self, alpha):
        self.res_surface.set_alpha(alpha)

    def setParam(self, params):
        if params[0]:
            self.res_Img = params[0]
        if params[1]:
            self.ClipRect = params[1]
        if params[2]:
            self.ColorKey = params[2]
        self.__buildSurface()


# 文字元素及其事件处理
class TextElement(Element):
    def __init__(self, area, text, font, size, color, antiAlias):
        super(TextElement, self).__init__(area)
        self.Font = font
        self.Text = text
        self.Size = size
        self.Color = color
        self.AntiAlias = antiAlias
        self.__buildSurface()

    # 这里是渲染非透明文本的方法，没有底色
    # def __buildSurface(self):
    #     textTemp = pygame.font.Font(self.Font, self.Size)
    #     self.res_surface = textTemp.render(self.Text, 1, self.Color)

    # 这里是渲染透明文本的方法, 无底色
    def __buildSurface(self):
        textTemp = pygame.font.Font(self.Font, self.Size)
        strList = self.Text.split('\n')
        self.res_surface = pygame.Surface((self.area.width, self.area.height)).convert()
        self.res_surface.fill((128, 128, 128))
        self.res_surface.set_colorkey((128, 128, 128))
        Line = 0
        for s in strList:
            if s is not None and s != '':
                self.res_surface.blit(textTemp.render(s, self.AntiAlias, self.Color),
                                      (0, Line * (self.Size + const_Text_LineSize)))
                Line += 1
        if len(self.Color) >= 4:
            self.res_surface.set_alpha(self.Color[3])

    def draw(self, screen):
        screen.blit(self.res_surface, (self.area.left, self.area.top))

    def setAlpha(self, alpha):
        self.res_surface.set_alpha(alpha)

    def setText(self, text):
        self.Text = text
        self.__buildSurface()

    def setFont(self, font):
        self.Font = font
        self.__buildSurface()

    def setSize(self, size):
        self.Size = size
        self.__buildSurface()

    def setColor(self, color):
        self.Color = color
        self.__buildSurface()

    def setParam(self, params):
        if params[0]:
            self.Text = params[0]
        if params[1]:
            self.Font = params[1]
        if params[2]:
            self.Size = params[2]
        if params[3]:
            self.Color = params[3]
        self.__buildSurface()


# 图像元素及其事件处理
class ImgElement(Element):
    def __init__(self, area, path, alpha=255, colorKey=None):
        super(ImgElement, self).__init__(area)
        self.Path = path
        self.Alpha = alpha
        self.ColorKey = colorKey
        self.__buildSurface()

    def __buildSurface(self):
        self.res_surface = pygame.image.load(self.Path)
        if self.ColorKey:
            self.res_surface.set_colorkey(self.ColorKey)

    def draw(self, screen):
        screen.blit(self.res_surface, (self.area.left, self.area.top))

    def setPath(self, path):
        self.Path = path
        self.__buildSurface()

    def setAlpha(self, alpha):
        self.res_surface.set_alpha(alpha)


# 序章场景

# 渲染单元
class RenderUnionElement(Element):
    def __init__(self, surface, pos, area):
        super(RenderUnionElement, self).__init__(area)
        self.res_surface = surface
        self.pos = pos


# 设置页面元素

# 鼠标左键按下鼠标改变元素位置事件
def Pos(e, isDown):
    if isDown:
        e.area.top += 1
        e.area.left += 1
    else:
        e.area.top -= 1
        e.area.left -= 1


class OptButtonElement(Element):
    def __init__(self, area, color):
        super(OptButtonElement, self).__init__(area)
        self.Color = color
        self.__buildSurface()

        self.Events.appendEvent(ioEvent3Enum.mouseIn, lambda: self.setAlpha(color[3] + 100), 0)
        self.Events.appendEvent(ioEvent3Enum.mouseOut, lambda: self.setAlpha(color[3]), 0)
        self.Events.appendEvent(ioEvent3Enum.mouseLeftKeyUp, lambda: Pos(self, False), 0)
        self.Events.appendEvent(ioEvent3Enum.mouseLeftKeyDown, lambda: Pos(self, True), 0)

    def __buildSurface(self):
        self.res_surface = blankSurface((self.area[2], self.area[3]), self.Color)

    def draw(self, screen):
        screen.blit(self.res_surface, (self.area.left, self.area.top))

    def setAlpha(self, alpha):
        self.res_surface.set_alpha(alpha)


# 选择按钮
class OptUIElement(ImgElement):
    def __init__(self, area, path, alpha=255):
        super(OptUIElement, self).__init__(area, path, alpha)

        self.Events.appendEvent(ioEvent3Enum.mouseLeftKeyUp, lambda: Pos(self, False), 0)
        self.Events.appendEvent(ioEvent3Enum.mouseLeftKeyDown, lambda: Pos(self, True), 0)


# 继续游戏界面

# 存储资料选项
class SaveDataElement(ImgElement):
    def __init__(self, area, path, alpha, lis):
        super(SaveDataElement, self).__init__(area, path, alpha)
        self.__buildBG((255, 255, 255, 100))
        self.__lis = lis
        print(self.__lis)
        self.__date = self.__lis[0]
        self.__time = self.__lis[1]
        self.__HP = self.__lis[2]
        self.__MP = self.__lis[3]
        self.__E_text_date = TextElement(area, self.__date, gl_Font_oth, 30, (0, 0, 0), 1)

        self.Events.appendEvent(ioEvent3Enum.mouseIn, lambda: self.__setBGAlpha(200), 0)
        self.Events.appendEvent(ioEvent3Enum.mouseOut, lambda: self.__setBGAlpha(100), 0)

    def __buildBG(self, color):
        self.__bg = blankSurface((self.area.width - 22, self.area.height - 22), color)

    def __setBGAlpha(self, alpha):
        self.__bg.set_alpha(alpha)

    def draw(self, screen):
        screen.blit(self.__bg, (self.area.left + 11, self.area.top + 11))
        super().draw(screen)
        self.__E_text_date.draw(screen)
