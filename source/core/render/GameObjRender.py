"""
sgf-py game object render

Element, Actor, 统称为gameObject
"""
import time

from source.core.const.Const import gl_LogPath
from source.view.baseClazz.Actor import Actor
from source.view.baseClazz.Element import Element


class gameObjRender:
    """在添加完毕后调用close()方法，然后才能渲染，下次添加时需调用open()方法

    如果出现异常，可调用getLog方法查看记录日志"""

    def __init__(self):
        self.__renderDict = {}
        self.__flag_add = True
        self.__sortedList = []
        self.__sortedRevList = []
        self.__objList = []
        self.__flag_record = True

        self.__log = 'Render Log: ' + time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime()) + \
                     self.__class__.__name__ + ' be created\n'
        self.__logFile = open(gl_LogPath + 'render.log', 'a')
        self.__logFile.write(self.__log)

    def __del__(self):
        self.__logFile.close()

    def __sortKey(self):
        temp = sorted(self.__renderDict.items(), key=lambda a: a[0])
        for tr in temp:
            for e in tr[1]:
                self.__sortedList.append(e)
        # for e in reversed(self.__sortedList):
        #     if e.active:
        #         self.__sortedRevList.append(e)
        self.__sortedRevList = list(reversed(self.__sortedList))

    def add(self, *args):
        if not self.__flag_add:
            self.__log += 'Render Log Error: render closed, add ' + str(args) + ' failed\n'
            self.__logFile.write('Render Log Error: render closed, add ' + str(args) + ' failed\n')
        else:
            self.__log += 'Render Log: ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' add start\n'
            self.__logFile.write('Render Log: ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' add start\n')
            self.__add(*args)
            self.__log += 'Render Log: ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' add finished\n'
            self.__logFile.write(
                'Render Log: ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' add finished\n')

    def remove(self, *args):
        if not self.__flag_add:
            self.__log += 'Render Log Error: render closed, remove ' + str(args) + ' failed\n'
            self.__logFile.write('Render Log Error: render closed, remove ' + str(args) + ' failed\n')
        else:
            self.__log += 'Render Log: ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' remove start\n'
            self.__logFile.write(
                'Render Log: ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' remove start\n')
            self.__remove(*args)
            self.__log += 'Render Log: ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' remove finished\n'
            self.__logFile.write(
                'Render Log: ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' remove finished\n')

    def update(self, index, *args):
        if not self.__flag_add:
            self.__log += 'Render Log Error: render closed, update ' + str(args) + ' failed\n'
            self.__logFile.write('Render Log Error: render closed, update ' + str(args) + ' failed\n')
        else:
            self.__log += 'Render Log: ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' update start\n'
            self.__logFile.write(
                'Render Log: ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' update start\n')
            self.__update(index, *args)
            self.__log += 'Render Log: ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' update finished\n'
            self.__logFile.write(
                'Render Log: ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' update finished\n')

    def __add(self, *args):
        if len(args) == 1:
            x = args[0]
            if isinstance(x, Element) or isinstance(x, Actor):
                z = x.zIndex
                if z in self.__renderDict.keys():
                    self.__renderDict[x.zIndex].append(x)
                else:
                    self.__renderDict[x.zIndex] = [x]
            elif isinstance(x, list) or isinstance(x, tuple):
                for e in x:
                    self.__add(e)
            else:
                self.__log += 'Render Log Error: ' + x.__class__.__name__ + ' is ' + str(
                    x.__class__) + ' cant insert render record list\n'
                self.__logFile.write(
                    'Render Log Error: ' + x.__class__.__name__ + ' is ' + str(
                        x.__class__) + ' cant insert render record list\n')
        else:
            for e in args:
                self.__add(e)

    def __remove(self, index, *args):
        if len(args) == 1:
            x = args[0]
            if isinstance(x, list) or isinstance(x, tuple):
                self.__remove(index, x)
            try:
                lis = self.__renderDict[index]
                lis.remove(x)
            except ValueError:
                self.__log += 'Render Log Error: remove value error ' + x.__class__.__name__ + ' \n'
                self.__logFile.write('Render Log Error: remove value error ' + x.__class__.__name__ + ' \n')
            except KeyError:
                self.__log += 'Render Log Error: remove index error ' + index + ' \n'
                self.__logFile.write('Render Log Error: index error remove ' + index + ' \n')
        else:
            for e in args:
                self.__remove(e)

    def __update(self, index, *args):
        self.__remove(index, *args)
        self.__add(*args)

    def close(self):
        if self.__flag_add:
            self.__sortKey()
            self.__flag_add = False
            self.__log += 'Render Log: ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' close\n'
            self.__logFile.write('Render Log: ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' close\n')
            self.__logFile.close()

    # def closeLog(self):
    #     self.__logFile.write(
    #         'Render Log: ' + time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime())
    #         + self.__class__.__name__ + ' be closed\n')
    #     self.__logFile.close()

    def open(self):
        self.__logFile = open(gl_LogPath + 'render.log', 'a')
        self.__flag_add = True
        self.__flag_record = True
        self.__log += 'Render Log: ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' open\n'
        self.__logFile.write('Render Log: ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' open\n')

    def getLog(self):
        return self.__log

    def renderList(self):
        return self.__sortedList

    def eventHandingList(self):
        return self.__sortedRevList

    def render(self, sur):
        if not self.__flag_add:
            for e in self.__sortedList:
                if e.visual:
                    e.draw(sur)
        elif self.__flag_record:
            self.__log += 'Render Log Error: should close before render\n'
            self.__logFile.write('Render Log Error: should close before render\n')
            self.__flag_record = False
