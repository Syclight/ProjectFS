import tkinter.filedialog
import tkinter.messagebox
from operator import eq

import pygame

from source.core.assembly.Anime import AnimeFrame, AnimePart
from source.core.const.Const import gl_Font_opt
from source.core.math.Shape import Rectangle
from source.core.math.Vector import vec2, vec4
from source.util.ToolsFuc import centeredXPos, centeredYPos, InElement
from source.view.baseClazz.Actor import Actor
from source.view.baseClazz.Element import Element
from source.view.baseClazz.Scene import Scene
from source.view.element.Control import InputElement
from source.view.element.Elements import TextElement, ioEvent3Enum, ImgElement


# def openFiledialog():
#     root = tkinter.Tk()
#     root.withdraw()
#     print(tkinter.filedialog.askopenfilenames(title='选择一个文件', filetypes=[('Images', '.jpg .jpge .bmp .png')])


# class Operation:
#     def __init__(self, name, width, height, _id):
#         texture = pygame.image.load(name)
#         texture_w = texture.get_rect().w
#         texture_h = texture.get_rect().h
#         area = Rectangle(centeredXPos(width, texture_w), centeredYPos(height, texture_h), texture_w, texture_h)
#         self.actor = Actor(texture, area)
#         self.element = ImgElement(area, name)
#         self.id = _id

class showImgWin(ImgElement):
    def __init__(self, area):
        super(showImgWin, self).__init__(area, path=None, alpha=255, colorKey=None)

    def showImg(self, currentOperation):
        _tex = currentOperation.getInitTexture()
        _texW = _tex.get_rect().w
        _texH = _tex.get_rect().h
        if _texH > _texW:
            scaleSizeY = self.area.size()[1]
            scaleSizeX = scaleSizeY / _texH * _texW
            blitLocal = (centeredXPos(self.area.w, scaleSizeX), 0)
        else:
            scaleSizeX = self.area.size()[0]
            scaleSizeY = scaleSizeX / _texW * _texH
            blitLocal = (0, centeredYPos(self.area.h, scaleSizeY))
        suf = pygame.transform.scale(_tex, (int(scaleSizeX), int(scaleSizeY)))
        self.clear((0, 0, 0))
        self.res_surface.blit(suf, blitLocal)


class butElement(TextElement):
    def __init__(self, area, text, font, size, color, antiAlias):
        super(butElement, self).__init__(area, text, font, size, color, antiAlias)
        self.zIndex = 999
        self.Events.appendEvent(ioEvent3Enum.mouseIn, lambda: self.__evn_chColor(1), 0)
        self.Events.appendEvent(ioEvent3Enum.mouseOut, lambda: self.__evn_chColor(0), 0)

    def __evn_chColor(self, isIn):
        if isIn:
            self.setColor((0, 162, 232))
        else:
            self.setColor((255, 255, 255))


class Operation(ImgElement):
    def __init__(self, name, bgWidth, bgHeight, _id):
        self.texture = pygame.image.load(name)
        self.__texture_w = self.texture.get_rect().w
        self.__texture_h = self.texture.get_rect().h
        area = Rectangle(centeredXPos(bgWidth, self.__texture_w), centeredYPos(bgHeight, self.__texture_h),
                         self.__texture_w, self.__texture_h)
        super(Operation, self).__init__(area, name)
        self.id = _id
        self.Interpolation = None
        self.InterpData = dict()
        self.__bkupTex = self.texture

        self.__AnimeSequence = list()
        self.__AnimeFrames = list()

        self.Events.appendEvent(ioEvent3Enum.mouseRollDown, lambda: self.__evn_downsizeTex(1), 0)
        self.Events.appendEvent(ioEvent3Enum.mouseRollUp, lambda: self.__evn_downsizeTex(0), 0)

        self.__index = 0

    # def showOperate(self):
    #

    def __evn_downsizeTex(self, typ):
        if typ:
            self.texture = pygame.transform.scale(self.__bkupTex, (
                int(self.__texture_w - 0.1 * self.__texture_w), int(self.__texture_h - 0.1 * self.__texture_h)))
        else:
            self.texture = pygame.transform.scale(self.__bkupTex, (
                int(self.__texture_w + 0.1 * self.__texture_w), int(self.__texture_h + 0.1 * self.__texture_h)))
        self.area = Rectangle(self.area.x, self.area.y, self.texture.get_rect().w,
                              self.texture.get_rect().h)
        self.__texture_w = self.area.w
        self.__texture_h = self.area.h
        self.res_surface = self.texture

    def getInitTexture(self):
        return self.__bkupTex

    def clearAnimeData(self):
        self.__AnimeFrames.clear()

    def record(self, time):
        _animeFrame = AnimeFrame(time, vec4(self.area.local(), self.area.size()))
        self.__AnimeFrames.append(_animeFrame)

    def showAnime(self):
        if len(self.__AnimeFrames) > 0:
            _frame = self.__AnimeFrames[self.__index]
            self.area.x = _frame.local.x
            self.area.y = _frame.local.y
            self.res_surface = pygame.transform.scale(self.__bkupTex, (int(_frame.local.z), int(_frame.local.w)))
            self.__index += 1
            if self.__index >= len(self.__AnimeFrames):
                self.__index = 0

    def getAnimeFrames(self):
        return self.__AnimeFrames

    # def __evn_enlargeTex(self):
    #     self.texture = pygame.transform.scale(self.texture, (
    #         int(self.__texture_w + 0.1 * self.__texture_w), int(self.__texture_h + 0.1 * self.__texture_h)))
    #     self.__texture_w = self.texture.get_rect().w
    #     self.__texture_h = self.texture.get_rect().h
    #     self.res_surface = self.texture

    # def draw(self, screen):
    #     screen.blit(texture)


class AnimaEditor(Scene):
    def __init__(self, *args):
        super(AnimaEditor, self).__init__(*args)
        self.caption = "sgf-py GUITools AnimeEditor GUI工具 动画编辑器"
        self.materialList = list()
        self.butOutput = butElement((10, 10, 34, 18), "导出", gl_Font_opt, 16, (255, 255, 255), 1)
        self.butInput = butElement((50, 10, 34, 18), "导入", gl_Font_opt, 16, (255, 255, 255), 1)
        self.butClear = butElement((90, 10, 34, 18), "清空", gl_Font_opt, 16, (255, 255, 255), 1)
        self.butDel = butElement((130, 10, 34, 18), "删除", gl_Font_opt, 16, (255, 255, 255), 1)
        self.butStart = butElement((170, 10, 34, 18), "开始", gl_Font_opt, 16, (255, 255, 255), 1)
        self.__flg_isStart = False
        self.butKeyFrame = butElement((210, 10, 82, 18), "设定关键帧", gl_Font_opt, 16, (255, 255, 255), 1)
        self.butSetTime = butElement((300, 10, 66, 18), "设定时间", gl_Font_opt, 16, (255, 255, 255), 1)
        self.butSetIntpol = butElement((370, 10, 66, 18), "插值方式", gl_Font_opt, 16, (255, 255, 255), 1)
        self.butHelp = butElement((440, 10, 34, 18), "帮助", gl_Font_opt, 16, (255, 255, 255), 1)

        self.currentShow = showImgWin((600, 0, 200, 150))
        self.currentShow.zIndex = 999

        self.butReshow = butElement((10, self.height - 30, 34, 18), "回放", gl_Font_opt, 16, (255, 255, 255), 1)
        self.__flg_reshow = False
        self.butReshowAll = butElement((50, self.height - 30, 66, 18), "全部回放", gl_Font_opt, 16, (255, 255, 255), 1)
        self.butClearData = butElement((120, self.height - 30, 66, 18), "清除数据", gl_Font_opt, 16, (255, 255, 255), 1)
        self.__flg_reshowAll = False

        self.__flg_currentShowIsDownsize = False
        self.currentShow.Events.appendEvent(ioEvent3Enum.mouseLeftKeyClick, lambda: self.__evn_scale(), 1)

        self.inputBox = InputElement((centeredXPos(self.width, 200), self.height - 30, 200, 20), "input")
        self.inputBox.zIndex = 999

        self.currtOp = None
        self.__prop_Interval = 1

        self.__recordStartTime = 0
        self.__index = 0

    def __evn_scale(self):
        if not self.__flg_currentShowIsDownsize:
            self.currentShow.area.x = 750
            self.__flg_currentShowIsDownsize = True
        else:
            self.currentShow.area.x = 600
            self.__flg_currentShowIsDownsize = False

    def setup(self):
        self.render.open()
        self.render.add(self.currentShow)
        self.render.add(self.butOutput)
        self.render.add(self.butInput)
        self.render.add(self.butClear)
        self.render.add(self.butDel)
        self.render.add(self.butStart)
        self.render.add(self.butKeyFrame)
        self.render.add(self.butSetTime)
        self.render.add(self.butSetIntpol)
        self.render.add(self.butReshow)
        self.render.add(self.butHelp)
        self.render.add(self.butReshowAll)
        self.render.add(self.butClearData)
        self.render.add(self.inputBox)
        self.render.close()
        self.id = 0

        self.butInput.Events.appendEvent(ioEvent3Enum.mouseLeftKeyClick, lambda: self.__evn_selMaterials(), 1)
        self.butOutput.Events.appendEvent(ioEvent3Enum.mouseLeftKeyClick, lambda: self.__evn_save(), 1)
        self.butClear.Events.appendEvent(ioEvent3Enum.mouseLeftKeyClick, lambda: self.__evn_clear(), 1)
        self.butDel.Events.appendEvent(ioEvent3Enum.mouseLeftKeyClick, lambda: self.__evn_del(), 1)
        self.butStart.Events.appendEvent(ioEvent3Enum.mouseLeftKeyClick, lambda: self.__evn_start(), 1)
        self.butSetTime.Events.appendEvent(ioEvent3Enum.mouseLeftKeyClick, lambda: self.__evn_setTime(), 1)
        self.butReshow.Events.appendEvent(ioEvent3Enum.mouseLeftKeyClick, lambda: self.__evn__reshow(), 1)
        self.butReshowAll.Events.appendEvent(ioEvent3Enum.mouseLeftKeyClick, lambda: self.__evn_reshowAll(), 1)
        self.butClearData.Events.appendEvent(ioEvent3Enum.mouseLeftKeyClick, lambda: self.__evn_clearData(), 1)

        self.createTextElement("", pos=self.BOTTOM_RIGHT, length=180, font=gl_Font_opt, color=(255, 127, 39))
        self.createTextElement("FPS:" + str(self.FPS), pos=self.TOP_RIGHT, font=gl_Font_opt, color=(255, 127, 39))

    def __evn_clearData(self):
        if self.currtOp:
            self.currtOp.clearAnimeData()
            self.getCreatedElement(0).setText("已删除对象动画数据")

    def __evn_reshowAll(self):
        if len(self.materialList) > 0:
            self.__flg_reshowAll = not self.__flg_reshowAll
            if self.__flg_reshowAll:
                self.butReshow.active = False
                self.getCreatedElement(0).setText("正在播放全部对象动画")
                self.butReshowAll.setText("全部暂停")
            else:
                self.butReshow.active = True
                self.getCreatedElement(0).setText("全部对象动画播放完毕")
                self.butReshowAll.setText("全部回放")

    def __evn__reshow(self):
        if len(self.materialList) > 0:
            self.__flg_reshow = not self.__flg_reshow
            if self.__flg_reshow:
                self.getCreatedElement(0).setText("正在播放当前对象动画")
                self.butReshow.setText("暂停")
            else:
                self.getCreatedElement(0).setText("当前对象动画播放完毕")
                self.butReshow.setText("回放")

    def __evn_setTime(self):
        def on_click():
            _interval_str = xls_text.get().lstrip()
            if len(_interval_str) != 0:
                try:
                    time_float = float(_interval_str)
                except ValueError:
                    return
                finally:
                    root.quit()
                    root.destroy()
                self.__prop_Interval = time_float
                self.caption += " interval:" + _interval_str

        # root = tkinter.Tk()
        root = tkinter.Tk()
        root.title("设定时间")
        xls_text = tkinter.StringVar()
        l1 = tkinter.Label(root, text="请输入时间，时间必须为整型或浮点数：")
        l1.pack()  # 这里的side可以赋值为LEFT  RTGHT TOP  BOTTOM
        xls = tkinter.Entry(root, textvariable=xls_text)
        xls_text.set(" ")
        xls.pack()
        tkinter.Button(root, text="确认", command=on_click).pack()
        root.mainloop()
        # root.withdraw()
        # tkinter.messagebox.askyesno(title='系统提示', message='是否需要')

    def __evn_start(self):
        if len(self.materialList) > 0:
            if self.__flg_reshow or self.__flg_reshowAll:
                self.getCreatedElement(0).setText("正在播放,无法录制")
                return
            if not self.__flg_isStart:
                # if not self.__flg_isStart and self.currtOp:
                self.__flg_isStart = True
                self.getCreatedElement(0).setText("已开始捕捉动画")
                self.butStart.setText("完成")
            else:
                self.__flg_isStart = False
                self.getCreatedElement(0).setText("捕捉动画停止")
                self.butStart.setText("开始")

    # def __evn_stop(self):
    #     if self.__flg_isStart:
    #         self.__flg_isStart = False
    #         self.getCreatedElement(0).setText("捕捉动画停止")

    def __evn_selMaterials(self):
        root = tkinter.Tk()
        root.withdraw()
        _nameTuple = tkinter.filedialog.askopenfilenames(title='选择一个文件', filetypes=[('Images', '.jpg .jpge .bmp .png'),
                                                                                    ('sgfPyAnimeData', '.anime')])
        for name in _nameTuple:
            op = Operation(name, self.width, self.height, self.id)
            op.Events.appendEvent(ioEvent3Enum.mouseLeftKeyDown, lambda: self.__evn_curt(), 1)
            op.Events.appendEvent(ioEvent3Enum.mouseRightKeyDown, lambda: self.__evn_start(), 1)
            self.materialList.append(op)
            self.render.open()
            self.render.add(op)
            self.render.close()
            self.id += 1

    def __evn_save(self):
        root = tkinter.Tk()
        root.withdraw()
        _nameTuple = tkinter.filedialog.asksaveasfile(filetypes=[('sgfPyAnimeData', '.anime')])

    def __evn_clear(self):
        self.render.clearLog()
        self.render.open()
        for e in self.materialList:
            self.render.remove(e.zIndex, e)
        self.render.close()
        self.materialList.clear()

    def __evn_curt(self):
        self.currtOp = self.focus
        self.__index = 0

    def __evn_del(self):
        if self.currtOp in self.materialList:
            self.materialList.remove(self.currtOp)
            self.render.open()
            self.render.remove(self.currtOp.zIndex, self.currtOp)
            self.render.close()

    def doMouseMotion(self, MouseRel, Buttons):
        if self.currtOp and eq(Buttons, (1, 0, 0)) and InElement(self.mousePos, self.currtOp):
            barycenter = self.currtOp.area.barycenter()
            barycenter.x += self.mousePos[0] - self.lastMousePos[0]
            barycenter.y += self.mousePos[1] - self.lastMousePos[1]
            self.currtOp.area.rebuildForBarycenter(barycenter)

    def doClockEvent(self, NowClock):
        self.getCreatedElement(1).setText("FPS:" + str(self.FPS))
        if self.currtOp:
            self.currentShow.showImg(self.currtOp)
        if self.currtOp and self.__flg_isStart:
            if self.__recordStartTime == 0:
                self.__recordStartTime = NowClock
            self.currtOp.record(NowClock - self.__recordStartTime)
        if self.currtOp and self.__flg_reshow:
            self.currtOp.showAnime()
        if self.__flg_reshowAll and len(self.materialList) > 0:
            self.__flg_reshow = False
            self.butReshow.setText("回放")
            for op in self.materialList:
                op.showAnime()

    def doKeyEvent(self, Key, Mod, Type, Unicode):
        if Type == 0:
            self.inputBox.Events.doKeyDown(Key)
        print(Key, chr(Key), Mod, Unicode)
