import time
from queue import Queue

import pygame
from numpy import random

from source.core.assembly.IOEvent import ioEvent3Enum, getAsciiByIOEvent3Enum
from source.core.math.MathConst import MAX_ZINDEX
from source.core.math.MathUtil import constrain
from source.util.ToolsFuc import blankSurface
from source.view.baseClazz.Element import Element
from source.view.element.Control import BlankElement, TextArea
from source.view.element.Elements import TextElement

commDict = {}
funny = ['大爷，我现场采访您一下，您这样晨跑锻炼坚持几年了？\n姑娘别挡道！我尿急！',
         '请问你是做什么工作的？\n哦。我的工作是杀僵尸。\n嗯？可是这个世界上没有僵尸啊！\n你以为它们是怎么没有的？',
         '中午去买菜，感觉都不太新鲜了。\n老板：早上刚到的，都新鲜的。\n我：这菜看着就蔫蔫的啊？！\n老板：从早上到现在，它以为没人要自己了，这不垂头丧气么！\n我。。。',
         '我问他：你今天怎么没上班儿啊？\n表弟：那大舌头老板说，让我上班的时候，顺路捎十块钱的“砂纸”，结果我听成了“烧纸”\n我：那也不至于开除你啊\n表弟又说：老板看我买错了，让拿出去扔了，\n'
         '我跟他说，留着吧，万一再用上呢？',
         '周末，我和男友还有闺蜜一起乘地铁，人很多，\n我在男友身后，闺蜜在男友前面，我脑子一抽，伸手在闺蜜臀部掐了一下，\n闺蜜回头含情脉脉的看了我男友一眼，然后往男友身边靠近了些！\n闺蜜你这。。。']


def registerComm(text, fuc):
    commDict[text] = fuc


def IsValidComm(text) -> bool:
    if text in commDict.keys():
        return True
    return False


def getCommBlock(text):
    if text:
        return CommBlock(1, 3, text, time.localtime())
    return None


class CommBlock:
    def __init__(self, level, type_, text, time_):
        self.__lv = level
        self.__type = type_
        self.__text = text
        self.__time = time_
        # runnable
        self.flag_isActive = False
        # suspend
        self.flag_isSuspend = False
        # new
        self.flag_isStart = False
        # dead
        self.flag_isDead = False
        # running
        self.flag_isPressing = False
        # valid
        self.flag_isValid = False


class CommMsgShowText(TextElement):
    def __init__(self, pos, width, margin_top, margin_left, font_size=14, color=(255, 255, 255)):
        super(CommMsgShowText, self).__init__((pos[0] + margin_top, pos[1] + margin_left, width, 0), '',
                                              'source/view/origin/res/console.ttf', font_size, color, 1)

    def appendMsg(self, msg):
        if not isinstance(msg, str):
            return
        lines = msg.split('\n')
        self.area.h = self.area.h + (len(lines) - 1) * (self.Size + self.LineSpace)
        self.setText(self.Text + msg)


class Scrollbar(Element):
    def __init__(self, *args):
        super(Scrollbar, self).__init__(*args)
        self.__bar = BlankElement((0, 0, self.area.w, self.area.h), (0, 0, 0, 100))
        self.res_surface = None
        self.__buildSurface()

    def __buildSurface(self):
        self.res_surface = self.__bar.res_surface

    def updateLength(self, step):
        self.area.y += step
        self.__bar.setSize((self.__bar.area.w, self.__bar.area.h - step))
        self.__buildSurface()

    def updatePos(self, up, step):
        t_step = int(constrain(step, 0, self.area.h))
        if up:
            self.area.y -= t_step
        else:
            self.area.y += t_step
        self.__buildSurface()


class Console(TextArea):
    def __init__(self, *args):
        super(Console, self).__init__(*args, font='source/view/origin/res/console.ttf',
                                      fontSize=14, fontColor=(255, 255, 255), bgColor=(0, 0, 0, 200),
                                      baseColor=(0, 0, 0, 200), textSpace=1)
        self.__version = '0.1'
        self.zIndex = MAX_ZINDEX
        self.visual = False
        self.active = False

        self.__commPtr = -1
        self.__inputList = []

        registerComm('clear', lambda: self.clearText())
        registerComm('cl', lambda: self.clearText())
        registerComm('do-some-funny', lambda: self.funny())

    def getVerStr(self):
        return self.__version

    def log(self, msg):
        self.appendText(msg)

    def logl(self, msg):
        self.appendText(str(msg) + '\n')

    def keyInput(self, key):
        _key = getAsciiByIOEvent3Enum(key)
        # print(_key)
        # 8 - 退格 
        # 9 - Tab 
        # 13 - 回车 
        # 16~18 - Shift, Ctrl, Alt 
        # 37~40 - 左上右下 
        # 35~36 - End Home 
        # 46 - Del 
        # 112~123 - F1 - F12 
        if _key == 8:
            _text = self.getText()[:-1]
            self.__text = ''
            self.clearText()
            self.appendText(_text)
        elif _key == 13:
            text = self.getText().split('\n')[-1]
            self.__inputList.append(text)
            self.__commPtr += 1
            self.appendText('\n')
            if IsValidComm(text):
                commDict[text]()
            elif not text == '':
                self.appendText('\'{}\' is a invalid command'.format(text) + '\n')
        elif 32 <= _key <= 126:
            self.appendText(chr(_key))
        elif _key == 273:
            if len(self.__inputList) > 0:
                self.appendLastLine(self.__inputList[self.__commPtr])
                self.__commPtr -= 1
                if self.__commPtr < 0:
                    self.__commPtr = 0
        elif _key == 274:
            if len(self.__inputList) > 0:
                self.appendLastLine(self.__inputList[self.__commPtr])
                self.__commPtr += 1
                if self.__commPtr >= len(self.__inputList):
                    self.__commPtr = len(self.__inputList) - 1

    def funny(self):
        self.logl(funny[random.randint(-1, 5)])

    def errorLog(self, text):
        self.appendText()

# class Console(Element):
#     def __init__(self, *args):
#         super(Console, self).__init__(*args)
#         self.__commPtr = 0
#         self.__commWindBg = BlankElement((self.area.w, self.area.h - 20), (255, 255, 255, 100))
#         self.__commShowMsg = CommMsgShowText((self.area.x, self.area.y), self.area.w - 20, 10, 10)
#         self.__commShowMsg_blit_y = self.__commShowMsg.area.y
#         self.__commShowMsgSlid = Scrollbar((self.area.w - 10, 0, 10, self.__commWindBg.area.h))
#         self.__inputWindBack = BlankElement((self.area.w, 20), (200, 200, 200, 100))
#         self.__inputText = TextElement((0, 0, self.area.w, 20), '', 'source/view/origin/res/console.ttf', 18, (0, 0, 0),
#                                        1)
#         self.__commNewQueue = Queue()
#         self.__commSuspendedQueue = Queue()
#         self.__commRunningQueue = Queue()
#         self.__commDeadQueue = Queue()
#         self.__commRunnableQueue = Queue()
#
#         self.res_surface = None
#         self.zIndex = MAX_ZINDEX
#         self.visual = False
#         self.active = False
#
#         self.__buildSurface()
#
#         self.Events.appendEvent(ioEvent3Enum.mouseRollUp, lambda: self.__event_updateScrollBarPos(), 1)
#
#     def __event_updateScrollBarPos(self):
#         self.__commShowMsgSlid.updatePos(True, 10)
#         self.__buildSurface()
#
#     def __buildSurface(self):
#         self.res_surface = pygame.Surface((int(self.area.w), int(self.area.h))).convert()
#         self.res_surface.blit(self.__commWindBg.res_surface, (0, 0))
#         self.res_surface.blit(self.__inputWindBack.res_surface, (0, self.area.h - 20))
#         if (self.__commShowMsg.area.h - self.__commShowMsg.area.y) > (self.__commWindBg.area.h - 10):
#             self.__commShowMsg_blit_y = self.__commShowMsg_blit_y - 20
#             self.res_surface.blit(self.__commShowMsg.res_surface, (10, self.__commShowMsg_blit_y))
#             self.__commShowMsgSlid.updateLength(10)
#             self.res_surface.blit(self.__commShowMsgSlid.res_surface,
#                                   (self.__commShowMsgSlid.area.x, self.__commShowMsgSlid.area.y))
#         else:
#             self.res_surface.blit(self.__commShowMsg.res_surface, (10, 10))
#
#     def setInputText(self, text):
#         self.__inputText.setText(text)
#         comm = getCommBlock(text)
#         if comm:
#             self.__commNewQueue.put(comm)
#         self.__buildSurface()
#
#     def print(self, text):
#         self.__commShowMsg.appendMsg(str(text))
#         self.__buildSurface()
#
#     def draw(self, screen):
#         screen.blit(self.res_surface, (self.area.x, self.area.y))
