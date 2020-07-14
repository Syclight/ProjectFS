import time
from operator import eq

from source.core.assembly.AssetsFile import AssetsFile, AssetsType
from source.core.assembly.IOEvent import ioEvent3Enum
from source.view.baseClazz.Scene import Scene
from source.view.element.Elements import TitleConstElement, TitleOptElement, TextElement, ImgElement, OptButtonElement, \
    OptUIElement, SaveDataElement
from source.core.const.Const import *
from source.core.assembly.RecordFile import RecordFile
from source.util.ToolsFuc import *
from moviepy.editor import *


# Logo场景
class LogoScene(Scene):
    def __init__(self, screen, config, clock, paramList=None):
        super().__init__(screen, config, clock, paramList)
        # 注册与该场景相关的场景
        from source.config.AppConfig import registerScene
        registerScene(SCENENUM_TITLE, TitleScene)

        self.Logo = 'IEELogo.bmp'
        self.__alpha = 0
        self.bg = pygame.image.load(gl_ImgPath + self.Logo)

        self.__step = 4
        self.__frameRate = self.config.getFrameRate()
        if self.__frameRate != 0:
            self.__step = 255 / (2 * self.__frameRate)

    def draw(self):
        if self.isReadyToEnter:
            self.__alpha -= self.__step
        else:
            self.__alpha += self.__step
        if self.__alpha > 255:
            self.isReadyToEnter = True
        if self.__alpha < 0:
            self.isEnd = True
            self.nextSceneNum = SCENENUM_TITLE
        blitAlpha(self.screen, self.bg, (0, 0), self.__alpha)


# 标题场景
class TitleScene(Scene):
    def __init__(self, screen, config, clock, paramList=None):
        # 注册场景
        super().__init__(screen, config, clock, paramList)
        self.useDefaultDraw = False
        from source.config.AppConfig import registerScene
        registerScene(SCENENUM_GAME_PROLOGUE, Title_PrologueScene)
        registerScene(SCENENUM_OPT, OptionScene)
        registerScene(SCENENUM_CONTINUE, Continue_Scene)

        self.alpha = 0
        self.flag = False
        self.isMusicPlay = False

        self.wave_bgm = 'titleBackground.wav'
        self.titleBgName = 'titleBg.bmp'
        self.titleOptionName = 'titleOpts.bmp'
        self.titleName = 'titleTop.bmp'
        self.__res_s_cloud = 'T_S_C.png'
        self.__ast_name = 'I_T.assets'

        self.res_wave_bgm = pygame.mixer.Sound(gl_MusicPath + self.wave_bgm)
        self.res_wave_bgm.set_volume(self.config.getVolumeBGM())
        self.bg = pygame.image.load(gl_ImgPath + self.titleBgName)
        self.res_optionNewGame = pygame.image.load(gl_ImgPath + self.titleOptionName)
        self.res_title = pygame.image.load(gl_ImgPath + self.titleName)
        self.__frameRate = self.config.getFrameRate()

        self.__expBoardText = AssetsFile(os.path.join(gl_AssetsPath, 'TitleScene')).decode(
            self.__ast_name, AssetsType.EXP)

        # 创建相应的Element
        self.__board = TitleConstElement((gl_WindowWidth - 380, gl_WindowHeight - 80, 380, 80),
                                         blankSurface((380, 180), (255, 255, 255, 100)))
        self.__title = TitleConstElement((0, 0, 465, 74), clipResImg(self.res_title, (0, 0, 465, 74), (0, 0, 0)))
        self.__text = TextElement((gl_WindowWidth - 380, gl_WindowHeight - 80, 380, 80), self.__expBoardText[0],
                                  gl_Font, 16, (0, 0, 0), self.config.getTextAntiAlias())
        self.__optNewGame = TitleOptElement((140, 140, 116, 30), self.res_optionNewGame, (0, 0, 116, 30),
                                            (128, 128, 128))
        self.__optContinue = TitleOptElement((125, 180, 116, 30), self.res_optionNewGame, (0, 116, 116, 30),
                                             (128, 128, 128))
        self.__optOption = TitleOptElement((130, 220, 116, 30), self.res_optionNewGame, (0, 232, 116, 30),
                                           (128, 128, 128))
        self.__optExit = TitleOptElement((135, 260, 61, 30), self.res_optionNewGame, (0, 348, 61, 30), (128, 128, 128))

        self.__spriteCloud = ImgElement((801, -120, 750, 396), gl_ImgPath + self.__res_s_cloud)
        self.__spriteCloud.zIndex = -1
        self.__step = 1

        self.render.add(self.__board, self.__title, self.__text, self.__optNewGame, self.__optContinue,
                        self.__optOption, self.__optExit, self.__spriteCloud)
        self.render.close()
        # 这里绑定和控件有交互的事件
        # ---NewGame选项绑定事件---
        self.__optNewGame.Events.appendEvent(ioEvent3Enum.mouseLeftKeyClick,
                                             lambda: self.__retSignalIsReadyToEnd(SCENENUM_GAME_PROLOGUE), 1)
        self.__optNewGame.Events.appendEvent(ioEvent3Enum.mouseIn,
                                             lambda: self.__changeBoardText(self.__expBoardText[1]), 1)
        self.__optNewGame.Events.appendEvent(ioEvent3Enum.mouseOut,
                                             lambda: self.__changeBoardText(self.__expBoardText[0]), 1)
        # ---Continue选项绑定事件---
        self.__optContinue.Events.appendEvent(ioEvent3Enum.mouseLeftKeyClick,
                                              lambda: self.__retSignalIsReadyToEnd(SCENENUM_CONTINUE), 1)
        self.__optContinue.Events.appendEvent(ioEvent3Enum.mouseIn,
                                              lambda: self.__changeBoardText(self.__expBoardText[2]), 1)
        self.__optContinue.Events.appendEvent(ioEvent3Enum.mouseOut,
                                              lambda: self.__changeBoardText(self.__expBoardText[0]), 1)
        # ---Option选项绑定事件---
        self.__optOption.Events.appendEvent(ioEvent3Enum.mouseLeftKeyClick,
                                            lambda: self.__retSignalIsReadyToEnd(SCENENUM_OPT), 1)
        self.__optOption.Events.appendEvent(ioEvent3Enum.mouseIn,
                                            lambda: self.__changeBoardText(self.__expBoardText[3]), 1)
        self.__optOption.Events.appendEvent(ioEvent3Enum.mouseOut,
                                            lambda: self.__changeBoardText(self.__expBoardText[0]), 1)
        # ---Exit选项绑定事件---
        self.__optExit.Events.appendEvent(ioEvent3Enum.mouseIn,
                                          lambda: self.__changeBoardText(self.__expBoardText[4]), 1)
        self.__optExit.Events.appendEvent(ioEvent3Enum.mouseOut,
                                          lambda: self.__changeBoardText(self.__expBoardText[0]), 1)
        self.__optExit.Events.appendEvent(ioEvent3Enum.mouseLeftKeyClick,
                                          lambda: pygame.event.post(pygame.event.Event(12)), 1)

        # 渲染参数
        self.__step_in = 2
        self.__step_out = 5
        if self.__frameRate != 0:
            self.__step_in = 255 / (2 * self.__frameRate)
            self.__step_out = 255 / (1.5 * self.__frameRate)

        # ---选项单独事件-开始---

    # 改变text渲染的文字
    def __changeBoardText(self, text):
        self.__text.setText(text)

    # 传递信号
    def __retSignalIsReadyToEnd(self, SceneNum):
        self.isReadyToEnd = True
        self.nextSceneNum = SceneNum

    # ---选项单独事件-结束---

    def draw(self):
        if not self.flag:
            self.alpha += self.__step_in
        if self.alpha >= 255:
            if not self.isMusicPlay:
                self.isMusicPlay = True
                self.res_wave_bgm.play(loops=-1)
            self.alpha = 255
            self.flag = True
        blitAlpha(self.screen, self.bg, (0, 0), self.alpha)
        if self.flag and not self.isReadyToEnd:
            # pass
            self.render.render(self.screen)
            # for e in self.__ElementsList:
            #     e.draw(self.screen)
        if self.isReadyToEnd:
            self.res_wave_bgm.fadeout(2000)
            if self.alpha > 0:
                self.alpha -= self.__step_out
                blitAlpha(self.screen, self.bg, (0, 0), self.alpha)
            if self.alpha <= 0:
                self.res_wave_bgm.stop()
                self.isMusicPlay = False
                self.isEnd = True

    def doClockEvent(self, NowClock):
        _x = self.__spriteCloud.area.x
        if _x < -750:
            self.__spriteCloud.area.x = 801
        # self.__step *= -1
        self.__spriteCloud.area.x -= self.__step
        # print((NowClock, _x))


# 新游戏序章场景
class Title_PrologueScene(Scene):
    def __init__(self, screen, config, clock, paramList=None):
        # 初始化场景参数
        super().__init__(screen, config, clock, paramList)

        # resource name
        self.res_Img1 = 'NG_F_SS_1.bmp'
        self.res_Img2 = 'NG_F_SS_2.bmp'
        self.Sound_PourWine = 'NG_F_SS_PW.wav'
        self.Sound_Cup = 'NG_F_SS_C.wav'
        self.Sound_Drink = 'NG_F_SS_D.wav'
        self.Sound_Weak = 'NG_F_SS_W.wav'
        self.Music_BGM = 'NG_F_SS_BGM.wav'

        # assets name
        self.__asf_name1 = 'T_P.assets'
        self.__asf_name2 = 'T_P_C.assets'

        # 注册场景
        from source.config.AppConfig import registerScene
        registerScene(SCENENUM_GAME_STARTCG, Prologue_StartCGScene)

        # 音频
        pygame.mixer.music.load(gl_MusicPath + "TP_F_SS_BGM.mp3")

        self.res_Sound_PourWine = pygame.mixer.Sound(gl_SoundPath + self.Sound_PourWine)
        self.res_Sound_PourWine.set_volume(self.config.getVolumeSound())

        self.res_Sound_Cup = pygame.mixer.Sound(gl_SoundPath + self.Sound_Cup)
        self.res_Sound_Cup.set_volume(self.config.getVolumeSound())

        self.res_Sound_Drink = pygame.mixer.Sound(gl_SoundPath + self.Sound_Drink)
        self.res_Sound_Drink.set_volume(self.config.getVolumeSound())

        self.res_Sound_Weak = pygame.mixer.Sound(gl_SoundPath + self.Sound_Weak)
        self.res_Sound_Weak.set_volume(self.config.getVolumeSound())

        self.res_Music_BGM = pygame.mixer.Sound(gl_MusicPath + self.Music_BGM)
        self.res_Music_BGM.set_volume(self.config.getVolumeBGM())

        # 其它元素
        self.__assetsFile = AssetsFile(os.path.join(gl_AssetsPath, 'PrologueScene'))
        self.__TextList = self.__assetsFile.decode(self.__asf_name1, AssetsType.SUB)
        self.__DialogueList = self.__assetsFile.decode(self.__asf_name2, AssetsType.SUB)

        self.__TextShow = TextElement((200, 460, 270, 18), self.__TextList[0], gl_Font_oth, 16, (255, 255, 255),
                                      self.config.getTextAntiAlias())
        self.__ImgShow = ImgElement((80, 0, 640, 480), gl_ImgPath + self.res_Img1)
        self.__DialogueShow = TextElement((0, 500, 430, 18), self.__DialogueList[0], gl_Font_oth, 16, (255, 255, 255),
                                          self.config.getTextAntiAlias())

        # 注册元素
        self.__ElementsList = []

        # 设定渲染时的参数
        self.__flag_Num = 0
        self.__flag_BGMPlayed = False
        self.now_time, self.interval = None, None
        self.__TextShow_Interval, self.__DialogueShow_Interval = 5000, 6000
        self.__alphaStep_Text, self.__alphaStep_Dia = 0, 0
        self.__index, self.__alpha = 0, 0
        self.__frameRate = self.config.getFrameRate()
        if self.__frameRate == 0:
            self.__alphaStep_Text = self.__TextShow_Interval / 1000 * 0.036
            self.__alphaStep_Dia = self.__DialogueShow_Interval / 1000 * 0.416
        else:
            self.__alphaStep_Text = 255 / (((self.__TextShow_Interval - 1500) / 1000) * self.__frameRate)
            self.__alphaStep_Dia = 255 / self.__frameRate

    def draw(self):
        self.now_time = pygame.time.get_ticks()
        self.interval = self.now_time - self.startClock

        if not self.isReadyToEnd:
            if self.__flag_Num == 0:
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.play()
                if self.interval > self.__TextShow_Interval:
                    self.__alpha = 0
                    self.startClock = pygame.time.get_ticks()
                    self.__index += 1
                    if self.__index >= len(self.__TextList):
                        self.__index = 0
                        self.__flag_Num = 1
                        self.__alpha = 0
                        pygame.mixer.music.stop()
                        self.__ElementsList = [self.__ImgShow, self.__DialogueShow]
                    else:
                        self.__TextShow.setText(self.__TextList[self.__index])
                self.__alpha += self.__alphaStep_Text
                self.__TextShow.setAlpha(self.__alpha)
                self.screen.blit(self.__TextShow.res_surface, (
                    centeredXPos(self.screen.get_width(), len(self.__TextShow.Text) * self.__TextShow.Size), 400))
            elif self.__flag_Num == 1:
                if not self.__flag_BGMPlayed:
                    self.res_Music_BGM.play()
                    self.__flag_BGMPlayed = True
                if self.__index == 0 or self.__index == 1:
                    self.__alpha += self.__alphaStep_Dia
                    self.__ImgShow.setAlpha(self.__alpha)
                    self.__DialogueShow.setAlpha(self.__alpha - self.__alphaStep_Dia * self.__frameRate)
                if self.interval > self.__DialogueShow_Interval:
                    self.__alpha = 0
                    self.startClock = pygame.time.get_ticks()
                    self.__index += 1
                    if self.__index >= len(self.__DialogueList):
                        self.res_Sound_Cup.play()
                        time.sleep(1.4)
                        self.isReadyToEnd = True
                    else:
                        self.__DialogueShow.setText(self.__DialogueList[self.__index])
                        if self.__index == 1:
                            self.res_Sound_Weak.play()
                            self.__ImgShow.setPath(gl_ImgPath + self.res_Img2)
                        if self.__index == 2:
                            self.res_Sound_Cup.play()
                        if self.__index == 3:
                            self.res_Sound_PourWine.play()
                        if self.__index == 4:
                            self.res_Sound_Drink.play()
                self.screen.blit(self.__ImgShow.res_surface, (self.__ImgShow.area.x, self.__ImgShow.area.y))
                self.screen.blit(self.__DialogueShow.res_surface, (
                    centeredXPos(self.screen.get_width(), len(self.__DialogueShow.Text) * self.__DialogueShow.Size),
                    self.__DialogueShow.area.y))
        else:
            self.nextSceneNum = SCENENUM_GAME_STARTCG
            self.isEnd = True


# 序章播放CG的场景，接下来的场景还没有编写，所以这里的下一个场景是开场Logo
class Prologue_StartCGScene(Scene):
    def __init__(self, screen, config, clock, paramList=None):
        super().__init__(screen, config, clock, paramList)
        self.__PrologueCG = 'P_M_PCG.mp4'
        # 视频
        self.__res_CG_clip = VideoFileClip(gl_VideoPath + self.__PrologueCG)

    def draw(self):
        if not self.isReadyToEnd:
            self.__res_CG_clip.preview()
            self.isReadyToEnd = True
        else:
            # 这里的下一个场景是开场Logo
            self.nextSceneNum = SCENENUM_INIT
            self.isEnd = True


def ChePos(e, isDown):
    if isDown:
        e.area.x += 1
        e.area.y += 1
    else:
        e.area.x -= 1
        e.area.y -= 1


class OptionScene(Scene):
    def __init__(self, screen, config, clock, paramList=None):
        super().__init__(screen, config, clock, paramList)

        self.__flag_isEnter = False
        self.__alpha = 0
        self.__flag_recordStartTime = False
        self.__start_time = 0
        self.__now_time = 0

        if paramList is not None:
            self.__flag_isEnter = paramList[0]

        # 注册与该场景相关的场景
        from source.config.AppConfig import registerScene
        registerScene(SCENENUM_OPT_APPLY, OptionScene, [True])

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
        self.__E_Text_Ret = TextElement((centeredXPos(80, 40, 50), centeredYPos(40, 20, 520), 120, 20), '返回',
                                        gl_Font_opt, 20, (0, 0, 0), self.config.getTextAntiAlias())

        self.__E_Text_Draw = TextElement((centeredXPos(200, 80, 40), centeredYPos(40, 20, 60), 80, 20), '画面设置',
                                         gl_Font_opt, 20, (0, 0, 0), self.config.getTextAntiAlias())
        self.__E_Text_AntiAlias = TextElement((270, 70, 120, 20), '抗锯齿：', gl_Font_opt, 18, (0, 0, 0),
                                              self.config.getTextAntiAlias())
        self.__E_Text_AA_Val = TextElement((670, 70, 20, 20), self.__KV_AA['key'], gl_Font_opt, 18, (0, 0, 0),
                                           self.config.getTextAntiAlias())

        self.__E_UI_AA_RightButton = OptUIElement((700, 70, 20, 20), gl_UIPath + self.res_UI_RightButton)
        self.__E_UI_AA_LeftButton = OptUIElement((640, 70, 20, 20), gl_UIPath + self.res_UI_LeftButton)
        self.__E_Text_Wave = TextElement((centeredXPos(200, 80, 40), centeredYPos(40, 20, 110), 80, 20), '声音设置',
                                         gl_Font_opt, 20, (0, 0, 0), self.config.getTextAntiAlias())
        self.__E_Text_BGMVolume = TextElement((270, 70, 120, 20), '音乐音量：', gl_Font_opt, 18, (0, 0, 0),
                                              self.config.getTextAntiAlias())
        self.__E_Text_BGM_Val = TextElement((660, 70, 30, 20), str(self.config.VolumeBGM), gl_Font_opt, 18, (0, 0, 0),
                                            self.config.getTextAntiAlias())
        self.__E_UI_BGM_RightButton = OptUIElement((700, 70, 20, 20), gl_UIPath + self.res_UI_RightButton)
        self.__E_UI_BGM_LeftButton = OptUIElement((630, 70, 20, 20), gl_UIPath + self.res_UI_LeftButton)
        self.__E_Text_SoundVolume = TextElement((270, 100, 120, 20), '音效音量：', gl_Font_opt, 18, (0, 0, 0),
                                                self.config.getTextAntiAlias())
        self.__E_Text_Sou_Val = TextElement((660, 100, 30, 20), str(self.config.VolumeSound), gl_Font_opt, 18,
                                            (0, 0, 0), self.config.getTextAntiAlias())
        self.__E_UI_Sou_RightButton = OptUIElement((700, 100, 20, 20), gl_UIPath + self.res_UI_RightButton)
        self.__E_UI_Sou_LeftButton = OptUIElement((630, 100, 20, 20), gl_UIPath + self.res_UI_LeftButton)

        self.__E_Text_Licence = TextElement(
            (centeredXPos(200, 120, 40), centeredYPos(40, 20, 160), 120, 20), '开源软件许可', gl_Font_opt, 20,
            (0, 0, 0), self.config.getTextAntiAlias())
        self.__E_Img_Licence = ImgElement(self.__E_BGBlankR.area, gl_ImgPath + 'OPT_L.lice', 255, (128, 128, 128))

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
        if not self.__flag_recordStartTime:
            self.__start_time = pygame.time.get_ticks()
            self.__flag_recordStartTime = True
        self.__now_time = pygame.time.get_ticks()

        blitAlpha(self.screen, self.res_Img_BG, (0, 0), self.__alpha)

        if not self.__flag_isEnter and not self.isReadyToEnd:
            self.__alpha += self.__step
            if self.__alpha >= 255:
                self.__alpha = 255
                self.__flag_isEnter = True
        elif self.__flag_isEnter and not self.isReadyToEnd:
            self.__alpha = 255
            for e in self.__ElementsMap['Draw']:
                e.draw(self.screen)
        if self.isReadyToEnd:
            self.isEnd = True

    def doMouseMotion(self, MouseRel, Buttons):
        # 鼠标移动事件
        for e in self.__ElementsMap['Interact']:
            if InElement(self.mousePos, e):
                self.focus = e
                if InElement(self.lastMousePos, e):
                    e.Events.doMouseMotion()
                elif eq(Buttons, (0, 0, 0)):
                    e.Events.doMouseIn()
            elif InElement(self.lastMousePos, e):
                e.Events.doMouseOut()
                if e.EventsHadDo.hadDoMouseLeftKeyDown:
                    e.Events.doMouseLeftKeyUp()
                    e.EventsHadDo.hadDoMouseLeftKeyDown = False
                    e.EventsHadDo.hadDoMouseLeftKeyUp = True


class Continue_Scene(Scene):
    __ElementsList = None

    def __init__(self, screen, config, clock, paramList=None):
        super().__init__(screen, config, clock, paramList)
        self.__ElementsList = []
        self.__mappingList = []
        self.__res_n_OPT = 'CTU_OPT.png'
        self.__buildList()

    def __buildList(self):
        fs = []
        import os
        for root, dirs, files in os.walk(RECORDFILE_SAVE_PATH):
            fs += files
        for name in fs:
            if name.find(RECORDFILE_SAVE_NAMEHEAD) == 0 and name.find(RECORDFILE_SAVE_EXN) > 0:
                n = name.replace(RECORDFILE_SAVE_EXN, '')
                dataList = RecordFile(RECORDFILE_SAVE_PATH, n).getList()
                if dataList is not None:
                    self.__ElementsList.append(
                        SaveDataElement((83, 30, 636, 114), gl_UIPath + self.__res_n_OPT, 255, dataList))
        if len(self.__ElementsList) == 0:
            self.__ElementsList.append(
                (TextElement((centeredXPos(800, 220), centeredXPos(600, 35), 220, 35), '未找到游戏记录', gl_Font_oth, 30,
                             (255, 255, 255, 255), self.config.getTextAntiAlias())))

    def __retSignalIsReadyToEnd(self, SceneNum):
        self.isReadyToEnd = True
        self.nextSceneNum = SceneNum

    def draw(self):
        if not self.isReadyToEnd:
            for e in self.__ElementsList:
                e.draw(self.screen)
        else:
            self.isEnd = True

    def doMouseMotion(self, MouseRel, Buttons):

        # 鼠标移动事件
        for e in self.__ElementsList:
            if InElement(self.mousePos, e):
                self.focus = e
                if InElement(self.lastMousePos, e):
                    e.Events.doMouseMotion()
                elif eq(Buttons, (0, 0, 0)):
                    e.Events.doMouseIn()
            elif InElement(self.lastMousePos, e):
                e.Events.doMouseOut()
                if e.EventsHadDo.hadDoMouseLeftKeyDown:
                    e.Events.doMouseLeftKeyUp()
                    e.EventsHadDo.hadDoMouseLeftKeyDown = False
                    e.EventsHadDo.hadDoMouseLeftKeyUp = True

    def doMouseButtonDownEvent(self, Button):
        if Button == 3:  # 左键
            self.__retSignalIsReadyToEnd(SCENENUM_TITLE)
