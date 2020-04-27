import pygame

from source.const.Const import gl_ImgPath, GLC_INI_NAME, GLC_INI_SECTION_WAVE, GLC_INI_PARAM_ANTIALIAS, \
    GLC_INI_SECTION_DRAW, GLC_INI_PARAM_BGMVOLUME, SCENENUM_TITLE, gl_Font_opt, gl_UIPath, GLC_INI_PARAM_SOUNDVOLUME, \
    SCENENUM_OPT_APPLY, gl_SoundPath
from source.core.assembly.IOEvent import ioEvent3Enum
from source.util.ToolsFuc import blitAlpha, updateINI, centeredYPos, centeredXPos, blankSurface
from source.view.baseClazz.Scene import Scene
from source.view.element.Elements import ImgElement, TextElement, TitleConstElement, OptButtonElement, \
    OptUIElement


def ChePos(e, isDown):
    if isDown:
        e.area.x += 1
        e.area.y += 1
    else:
        e.area.x -= 1
        e.area.y -= 1


class pickTest(Scene):
    def __init__(self, *args):
        super(pickTest, self).__init__(*args)

        self.__flag_isEnter = False
        self.__alpha = 0
        self.__flag_recordStartTime = False
        self.__start_time = 0
        self.__now_time = 0

        self.res_Img_BG_Name = 'OPT_BG.bmp'
        self.res_Sound_Choose_Name = 'OPT_C.wav'
        self.res_UI_RightButton = 'OPT_BR.png'
        self.res_UI_LeftButton = 'OPT_BL.png'

        self.__Clock = pygame.time.Clock()
        self.__KV_AA = {}
        self.__KV_WAVE = {}
        self.__ElementsMap = {}

        if self.config.getTextAntiAlias():
            self.__KV_AA['key'] = '开'
            self.__KV_AA['val'] = '1'
        else:
            self.__KV_AA['key'] = '关'
            self.__KV_AA['val'] = '0'

        self.res_Sound_Choose = pygame.mixer.Sound(gl_SoundPath + self.res_Sound_Choose_Name)
        self.res_Sound_Choose.set_volume(self.config.getVolumeSound())

        self.res_Img_BG = pygame.image.load(gl_ImgPath + self.res_Img_BG_Name)

        self.__E_BGBlankL1 = OptButtonElement((40, 60, 200, 40), (255, 255, 255, 100))
        self.__E_BGBlankL2 = OptButtonElement((40, 110, 200, 40), (255, 255, 255, 100))
        self.__E_BGBlankL3 = OptButtonElement((40, 160, 200, 40), (255, 255, 255, 100))
        self.__E_BGBlankLRet = OptButtonElement((50, 520, 80, 40), (255, 255, 255, 100))
        self.__E_BGBlankLApply = OptButtonElement((150, 520, 80, 40), (255, 255, 255, 100))
        self.__E_BGBlankR = TitleConstElement((260, 60, 510, 500), blankSurface((510, 500), (255, 255, 255, 100)))
        self.__E_Text_Apply = TextElement((centeredXPos(80, 40, 150), centeredYPos(40, 20, 520), 120, 20), '应用',
                                          gl_Font_opt, 20, (0, 0, 0), self.config.getTextAntiAlias())
        self.__E_Text_Apply.zIndex = 1
        self.__E_Text_Ret = TextElement((centeredXPos(80, 40, 50), centeredYPos(40, 20, 520), 120, 20), '返回',
                                        gl_Font_opt, 20, (0, 0, 0), self.config.getTextAntiAlias())
        self.__E_Text_Ret.zIndex = 1

        self.__E_Text_Draw = TextElement((centeredXPos(200, 80, 40), centeredYPos(40, 20, 60), 80, 20), '画面设置',
                                         gl_Font_opt, 20, (0, 0, 0), self.config.getTextAntiAlias())
        self.__E_Text_Draw.zIndex = 1
        self.__E_Text_AntiAlias = TextElement((270, 70, 120, 20), '抗锯齿：', gl_Font_opt, 18, (0, 0, 0),
                                              self.config.getTextAntiAlias())
        self.__E_Text_AntiAlias.zIndex = 1
        self.__E_Text_AA_Val = TextElement((670, 70, 20, 20), self.__KV_AA['key'], gl_Font_opt, 18, (0, 0, 0),
                                           self.config.getTextAntiAlias())
        self.__E_Text_AA_Val.zIndex = 1
        self.__E_UI_AA_RightButton = OptUIElement((700, 70, 20, 20), gl_UIPath + self.res_UI_RightButton)
        self.__E_UI_AA_RightButton.zIndex = 1
        self.__E_UI_AA_LeftButton = OptUIElement((640, 70, 20, 20), gl_UIPath + self.res_UI_LeftButton)
        self.__E_UI_AA_LeftButton.zIndex = 1
        self.__E_Text_Wave = TextElement((centeredXPos(200, 80, 40), centeredYPos(40, 20, 110), 80, 20), '声音设置',
                                         gl_Font_opt, 20, (0, 0, 0), self.config.getTextAntiAlias())
        self.__E_Text_Wave.zIndex = 1
        self.__E_Text_BGMVolume = TextElement((270, 70, 120, 20), '音乐音量：', gl_Font_opt, 18, (0, 0, 0),
                                              self.config.getTextAntiAlias())
        self.__E_Text_BGMVolume.zIndex = 1
        self.__E_Text_BGM_Val = TextElement((660, 70, 30, 20), str(self.config.VolumeBGM), gl_Font_opt, 18, (0, 0, 0),
                                            self.config.getTextAntiAlias())
        self.__E_Text_BGM_Val.zIndex = 1
        self.__E_UI_BGM_RightButton = OptUIElement((700, 70, 20, 20), gl_UIPath + self.res_UI_RightButton)
        self.__E_UI_BGM_RightButton.zIndex = 1
        self.__E_UI_BGM_LeftButton = OptUIElement((630, 70, 20, 20), gl_UIPath + self.res_UI_LeftButton)
        self.__E_UI_BGM_LeftButton.zIndex = 1
        self.__E_Text_SoundVolume = TextElement((270, 100, 120, 20), '音效音量：', gl_Font_opt, 18, (0, 0, 0),
                                                self.config.getTextAntiAlias())
        self.__E_Text_SoundVolume.zIndex = 1
        self.__E_Text_Sou_Val = TextElement((660, 100, 30, 20), str(self.config.VolumeSound), gl_Font_opt, 18,
                                            (0, 0, 0), self.config.getTextAntiAlias())
        self.__E_Text_Sou_Val.zIndex = 1
        self.__E_UI_Sou_RightButton = OptUIElement((700, 100, 20, 20), gl_UIPath + self.res_UI_RightButton)
        self.__E_UI_Sou_RightButton.zIndex = 1
        self.__E_UI_Sou_LeftButton = OptUIElement((630, 100, 20, 20), gl_UIPath + self.res_UI_LeftButton)
        self.__E_UI_Sou_LeftButton.zIndex = 1

        self.__E_Text_Licence = TextElement(
            (centeredXPos(200, 120, 40), centeredYPos(40, 20, 160), 120, 20), '开源软件许可', gl_Font_opt, 20,
            (0, 0, 0), self.config.getTextAntiAlias())
        self.__E_Text_Licence.zIndex = 1
        self.__E_Img_Licence = ImgElement(self.__E_BGBlankR.area, gl_ImgPath + 'OPT_L.lice', 255, (128, 128, 128))
        self.__E_Img_Licence.zIndex = 1

        # 画面设置绑定事件
        self.__E_BGBlankL1.Events.appendEvent(ioEvent3Enum.mouseLeftKeyDown, lambda: ChePos(self.__E_Text_Draw, True),
                                              1)
        self.__E_BGBlankL1.Events.appendEvent(ioEvent3Enum.mouseLeftKeyDown, lambda: self.__rebuildElementsToList2(
            [self.__E_Text_AntiAlias, self.__E_Text_AA_Val, self.__E_UI_AA_RightButton, self.__E_UI_AA_LeftButton]), 2)
        self.__E_BGBlankL1.Events.appendEvent(ioEvent3Enum.mouseLeftKeyUp, lambda: ChePos(self.__E_Text_Draw, False), 1)

        # 声音设置绑定事件
        self.__E_BGBlankL2.Events.appendEvent(ioEvent3Enum.mouseLeftKeyDown, lambda: ChePos(self.__E_Text_Wave, True),
                                              1)
        self.__E_BGBlankL2.Events.appendEvent(ioEvent3Enum.mouseLeftKeyDown, lambda: self.__rebuildElementsToList2(
            [self.__E_Text_BGMVolume, self.__E_Text_SoundVolume, self.__E_Text_BGM_Val, self.__E_Text_Sou_Val,
             self.__E_UI_BGM_RightButton, self.__E_UI_BGM_LeftButton, self.__E_UI_Sou_RightButton,
             self.__E_UI_Sou_LeftButton]), 2)
        self.__E_BGBlankL2.Events.appendEvent(ioEvent3Enum.mouseLeftKeyUp, lambda: ChePos(self.__E_Text_Wave, False), 1)

        # 开源软件许可按钮绑定事件
        self.__E_BGBlankL3.Events.appendEvent(ioEvent3Enum.mouseLeftKeyDown,
                                              lambda: ChePos(self.__E_Text_Licence, True), 1)
        self.__E_BGBlankL3.Events.appendEvent(ioEvent3Enum.mouseLeftKeyDown,
                                              lambda: self.__rebuildElementsToList2([self.__E_Img_Licence]), 2)
        self.__E_BGBlankL3.Events.appendEvent(ioEvent3Enum.mouseLeftKeyUp, lambda: ChePos(self.__E_Text_Licence, False),
                                              1)

        # 应用按钮绑定事件
        self.__E_BGBlankLApply.Events.appendEvent(ioEvent3Enum.mouseLeftKeyDown,
                                                  lambda: ChePos(self.__E_Text_Apply, True), 1)
        self.__E_BGBlankLApply.Events.appendEvent(ioEvent3Enum.mouseLeftKeyUp,
                                                  lambda: ChePos(self.__E_Text_Apply, False), 1)
        self.__E_BGBlankLApply.Events.appendEvent(ioEvent3Enum.mouseLeftKeyClick,
                                                  lambda: self.__retSignalIsReadyToEnd(SCENENUM_OPT_APPLY), 1)
        self.__E_BGBlankLApply.Events.appendEvent(ioEvent3Enum.mouseLeftKeyClick, lambda: self.__updConfig(), 2)

        # 返回按钮绑定事件
        self.__E_BGBlankLRet.Events.appendEvent(ioEvent3Enum.mouseLeftKeyDown, lambda: ChePos(self.__E_Text_Ret, True),
                                                1)
        self.__E_BGBlankLRet.Events.appendEvent(ioEvent3Enum.mouseLeftKeyUp, lambda: ChePos(self.__E_Text_Ret, False),
                                                1)
        self.__E_BGBlankLRet.Events.appendEvent(ioEvent3Enum.mouseLeftKeyClick,
                                                lambda: self.__retSignalIsReadyToEnd(SCENENUM_TITLE), 1)

        # 抗锯齿UI按钮绑定事件
        self.__E_UI_AA_LeftButton.Events.appendEvent(ioEvent3Enum.mouseLeftKeyClick, lambda: self.__chVal_AA_Txt(), 1)
        self.__E_UI_AA_RightButton.Events.appendEvent(ioEvent3Enum.mouseLeftKeyClick, lambda: self.__chVal_AA_Txt(), 1)

        # 改变音量UI按钮绑定事件
        self.__E_UI_BGM_LeftButton.Events.appendEvent(ioEvent3Enum.mouseLeftKeyClick,
                                                      lambda: self.__chVal_WaveParam_Txt(self.__E_Text_BGM_Val, False,
                                                                                         GLC_INI_PARAM_BGMVOLUME), 1)
        self.__E_UI_BGM_RightButton.Events.appendEvent(ioEvent3Enum.mouseLeftKeyClick,
                                                       lambda: self.__chVal_WaveParam_Txt(self.__E_Text_BGM_Val, True,
                                                                                          GLC_INI_PARAM_BGMVOLUME), 1)
        self.__E_UI_Sou_LeftButton.Events.appendEvent(ioEvent3Enum.mouseLeftKeyClick,
                                                      lambda: self.__chVal_WaveParam_Txt(self.__E_Text_Sou_Val, False,
                                                                                         GLC_INI_PARAM_SOUNDVOLUME), 1)
        self.__E_UI_Sou_RightButton.Events.appendEvent(ioEvent3Enum.mouseLeftKeyClick,
                                                       lambda: self.__chVal_WaveParam_Txt(self.__E_Text_Sou_Val, True,
                                                                                          GLC_INI_PARAM_SOUNDVOLUME), 1)

        self.__ElementsMap['Draw1'] = [self.__E_BGBlankL1, self.__E_BGBlankL2, self.__E_BGBlankL3, self.__E_BGBlankR,
                                       self.__E_Text_Draw, self.__E_Text_Wave, self.__E_Text_Licence,
                                       self.__E_BGBlankLApply,
                                       self.__E_Text_Apply, self.__E_BGBlankLRet, self.__E_Text_Ret]
        self.__ElementsMap['Draw2'] = [self.__E_Text_AntiAlias, self.__E_Text_AA_Val, self.__E_UI_AA_RightButton,
                                       self.__E_UI_AA_LeftButton]
        self.__ElementsMap['Interact1'] = [self.__E_BGBlankL1, self.__E_BGBlankL2, self.__E_BGBlankL3,
                                           self.__E_BGBlankLApply, self.__E_BGBlankLRet]
        self.__ElementsMap['Interact2'] = [self.__E_UI_AA_RightButton, self.__E_UI_AA_LeftButton]

        self.__ElementsMap['Draw'] = self.__ElementsMap['Draw1'] + self.__ElementsMap['Draw2']
        self.__ElementsMap['Interact'] = self.__ElementsMap['Interact1'] + self.__ElementsMap['Interact2']

        self.render.add(self.__ElementsMap['Draw1'])
        self.render.add(self.__ElementsMap['Interact'])
        self.render.close()

        # 设定渲染参数
        self.__step = 4
        self.__frameRate = self.config.getFrameRate()
        if self.__frameRate:
            self.__step = 255 / (1.5 * self.__frameRate)

    # 替换ElementsList2的内容
    def __rebuildElementsToList2(self, _list):
        if _list is None or len(_list) <= 0:
            return
        self.__ElementsMap['Draw2'] = _list
        self.__ElementsMap['Interact2'].clear()
        for e in _list:
            if e.Events.getSize() > 0:
                self.__ElementsMap['Interact2'].append(e)
        self.__ElementsMap['Draw'] = self.__ElementsMap['Draw1'] + self.__ElementsMap['Draw2']
        self.__ElementsMap['Interact'] = self.__ElementsMap['Interact1'] + self.__ElementsMap['Interact2']

    # 改变抗锯齿UI所对应的值
    def __chVal_AA_Txt(self):
        if self.__KV_AA['val'] == '1':
            self.__KV_AA['key'] = '关'
            self.__KV_AA['val'] = '0'
        else:
            self.__KV_AA['key'] = '开'
            self.__KV_AA['val'] = '1'
        self.__E_Text_AA_Val.setText(self.__KV_AA['key'])

    # 改变Wave UI所对应的值
    def __chVal_WaveParam_Txt(self, elem, add, para):
        valF = float(elem.Text)
        if add:
            valF += 0.5
            if valF > 10:
                valF = 10.0
        else:
            valF -= 0.5
            if valF < 0:
                valF = 0.0
        self.__KV_WAVE[para] = str(valF)
        elem.setText(self.__KV_WAVE[para])

    # 序列化值更新设置文件
    def __updConfig(self):
        updateINI(GLC_INI_NAME, GLC_INI_SECTION_DRAW, GLC_INI_PARAM_ANTIALIAS, self.__KV_AA['val'])
        for k, v in self.__KV_WAVE.items():
            updateINI(GLC_INI_NAME, GLC_INI_SECTION_WAVE, k, v)

    # 传递信号
    def __retSignalIsReadyToEnd(self, SceneNum):
        self.isReadyToEnd = True
        self.nextSceneNum = SceneNum

    def draw(self):
        blitAlpha(self.screen, self.res_Img_BG, (0, 0), self.__alpha)

        if not self.__flag_isEnter and not self.isReadyToEnd:
            self.__alpha += self.__step
            if self.__alpha >= 255:
                self.__alpha = 255
                self.__flag_isEnter = True
        elif self.__flag_isEnter and not self.isReadyToEnd:
            self.__alpha = 255
            self.render.render(self.screen)
        if self.isReadyToEnd:
            self.isEnd = True
