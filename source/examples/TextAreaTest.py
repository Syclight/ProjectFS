import pygame

from source.core.const.Const import gl_Font
from source.view.baseClazz.Scene import Scene
from source.view.element.Control import TextArea


class TextAreaTest(Scene):
    def __init__(self, *args):
        super(TextAreaTest, self).__init__(*args)
        self.__ta = TextArea((200, 100, 600, 600),  bgColor=(0, 0, 0, 200), fontColor=(255, 255, 255), slidColor=(255, 255, 255, 100))

    def setup(self):
        self.fillColor = (128, 0, 128)
        self.__ta.appendText('你好，\n'
                             '我是asheor:\n'
                             '   我尊敬的先生，很高兴能和你互通信件。我有一件事想要请教您。\n'
                             '是关于DirectRenderPipeline, \n'
                             '在一条管线中如何分配多个obj的顶点目标是非常令人费解的。')
        # self.__ta.appendText('你好Jack')
        self.render.open()
        self.render.add(self.__ta)
        self.render.close()
