from operator import eq

from Manager.IOEventManager import IOEventManager
from clazz.Config import Config
from clazz.Element import *
from clazz.Const import *
from clazz.ToolsFuc import *
from moviepy.editor import *


class Scene:
    def draw(self):
        pass

    def doMouseMotion(self, MousePos, MouseRel, Buttons):
        pass

    def doMouseButtonDownEvent(self, MousePos, Button):
        pass

    def doMouseButtonUpEvent(self, MousePos, Button):
        pass

    def doKeyEvent(self):
        pass


# Logo场景
class LogoScene(Scene):
    __screen = None
    isEnd = False
    MousePos = (0, 0)

    LogoName = 'IEELogo.bmp'
    bg = None

    nextSceneNum = 0

    def __init__(self, screen, paramList=None):
        # 注册与该场景相关的场景
        from clazz.AppConfig import registerScene
        registerScene(SCREEN_TITLE, TitleScene)

        self.__alpha = 0
        self.__flag = False
        self.__screen = screen
        self.bg = pygame.image.load(gl_ImgPath + self.LogoName)

    def draw(self):
        if self.__flag:
            self.__alpha -= 4
        else:
            self.__alpha += 4
        if self.__alpha > 255:
            self.__flag = True
        if self.__alpha < 0:
            self.isEnd = True
            self.nextSceneNum = SCREEN_TITLE
        blitAlpha(self.__screen, self.bg, (0, 0), self.__alpha)


# 标题场景
class TitleScene(Scene):
    __screen = None
    __ElementsList = None
    __Config = None
    __Focus = None
    __Focus_onClick = None

    alpha = None
    flag = None
    isReadyToEnd = None
    isEnd = None

    isMusicPlay = None

    MousePos = None

    wave_bgm = None
    titleBgName = None
    optionNewGame = None
    titleName = None
    bg = None
    res_optionNewGame = None
    res_title = None
    res_wave_bgm = None

    # surface Elements
    __title = None
    __optNewGame = None
    __optContinue = None
    __optOption = None
    __optExit = None
    __board = None
    __text = None

    nextSceneNum = None

    def __init__(self, screen, paramList=None):
        # 注册场景
        from clazz.AppConfig import registerScene
        registerScene(SCREEN_GAME_FIRSTSTORY, NewGame_First_StoryScene)
        registerScene(SCREEN_OPT, OptionScene)

        self.alpha = 0
        self.flag = False
        self.isReadyToEnd = False
        self.isEnd = False
        self.isMusicPlay = False

        self.MousePos = (0, 0)

        self.wave_bgm = 'titleBackground.wav'
        self.titleBgName = 'titleBg.bmp'
        self.optionNewGame = 'titleOpts.bmp'
        self.titleName = 'titleTop.bmp'

        self.nextSceneNum = 0

        self.__Focus = None
        self.__Focus_onClick = 0
        self.__screen = screen
        self.__Config = Config()
        self.res_wave_bgm = pygame.mixer.Sound(gl_MusicPath + self.wave_bgm)
        self.res_wave_bgm.set_volume(self.__Config.getVolumeBGM())
        self.bg = pygame.image.load(gl_ImgPath + self.titleBgName)
        self.res_optionNewGame = pygame.image.load(gl_ImgPath + self.optionNewGame)
        self.res_title = pygame.image.load(gl_ImgPath + self.titleName)
        # 创建相应的Element
        self.__board = TitleConstElement(pygame.Rect(gl_WindowWidth - 380, gl_WindowHeight - 80, 380, 80),
                                         blankSurface((380, 180), (255, 255, 255, 100)))
        self.__title = TitleConstElement(pygame.Rect(0, 0, 465, 74),
                                         clipResImg(self.res_title, pygame.Rect(0, 0, 465, 74), (0, 0, 0)))
        self.__text = TextElement(pygame.Rect(gl_WindowWidth - 380, gl_WindowHeight - 80, 380, 80),
                                  const_Text_titlePage_initShow, gl_Font, 16, (0, 0, 0),
                                  self.__Config.getTextAntiAlias())
        self.__optNewGame = TitleOptElement(pygame.Rect(140, 140, 116, 30),
                                            self.res_optionNewGame, pygame.Rect(0, 0, 116, 30),
                                            (128, 128, 128))
        self.__optContinue = TitleOptElement(pygame.Rect(125, 180, 116, 30),
                                             self.res_optionNewGame, pygame.Rect(0, 116, 116, 30),
                                             (128, 128, 128))
        self.__optOption = TitleOptElement(pygame.Rect(130, 220, 116, 30),
                                           self.res_optionNewGame, pygame.Rect(0, 232, 116, 30),
                                           (128, 128, 128))
        self.__optExit = TitleOptElement(pygame.Rect(135, 260, 61, 30),
                                         self.res_optionNewGame, pygame.Rect(0, 348, 61, 30), (128, 128, 128))

        # self.__ExitMessageBox = MessageBox(gl_WindowWidth, gl_WindowHeight, '确定要结束程序吗？')

        # 将全部element记录到列表中
        self.__ElementsList = [self.__board, self.__title, self.__text, self.__optNewGame, self.__optContinue,
                               self.__optOption, self.__optExit]
        # 这里绑定和控件有交互的事件
        # ---NewGame选项绑定事件---
        self.__optNewGame.Events.mouseLeftKeyClick.append(lambda: self.__retSignalIsReadyToEnd(SCREEN_GAME_FIRSTSTORY))
        self.__optNewGame.Events.mouseIn.append(lambda: self.__changeBoardText(const_Text_titlePage_NewGame))
        self.__optNewGame.Events.mouseOut.append(lambda: self.__changeBoardText(const_Text_titlePage_initShow))
        # ---Continue选项绑定事件---
        self.__optContinue.Events.mouseIn.append(lambda: self.__changeBoardText(const_Text_titlePage_Continue))
        self.__optContinue.Events.mouseOut.append(lambda: self.__changeBoardText(const_Text_titlePage_initShow))
        # ---Option选项绑定事件---
        self.__optOption.Events.mouseLeftKeyClick.append(lambda: self.__retSignalIsReadyToEnd(SCREEN_OPT))
        self.__optOption.Events.mouseIn.append(lambda: self.__changeBoardText(const_Text_titlePage_Option))
        self.__optOption.Events.mouseOut.append(lambda: self.__changeBoardText(const_Text_titlePage_initShow))
        # ---Exit选项绑定事件---
        self.__optExit.Events.mouseIn.append(lambda: self.__changeBoardText(const_Text_titlePage_Exit))
        self.__optExit.Events.mouseOut.append(lambda: self.__changeBoardText(const_Text_titlePage_initShow))
        self.__optExit.Events.mouseLeftKeyClick.append(lambda: pygame.event.post(pygame.event.Event(pygame.QUIT)))

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
            self.alpha += 2
        if self.alpha >= 255:
            if not self.isMusicPlay:
                self.isMusicPlay = True
                self.res_wave_bgm.play(loops=-1)
            self.alpha = 255
            self.flag = True
        blitAlpha(self.__screen, self.bg, (0, 0), self.alpha)
        if self.flag and not self.isReadyToEnd:
            for e in self.__ElementsList:
                e.draw(self.__screen)
                # self.__screen.blit(e.res_surface, (e.area.left, e.area.top))
        if self.isReadyToEnd:
            self.res_wave_bgm.fadeout(2000)
            if self.alpha > 0:
                self.alpha -= 5
                blitAlpha(self.__screen, self.bg, (0, 0), self.alpha)
            if self.alpha <= 0:
                self.res_wave_bgm.stop()
                self.isMusicPlay = False
                self.isEnd = True

    def doMouseMotion(self, MousePos, MouseRel, Buttons):
        if not eq(Buttons, (0, 0, 0)) or self.__ElementsList is None:
            return
        if len(self.__ElementsList) > 0 and self.__Focus is None:
            for e in self.__ElementsList:
                if InElement(MousePos, e):
                    self.__Focus = e
                    self.__Focus.Events.doMouseIn()
                    print('确定焦点元素：', self.__Focus.area, '\n鼠标位置：', MousePos)
                    break
        if not InElement(MousePos, self.__Focus) and self.__Focus is not None:
            self.__Focus.Events.doMouseOut()
            if self.__Focus.EventsHadDo.hadDoMouseLeftKeyDown:
                self.__Focus.EventsHadDo.hadDoMouseLeftKeyDown = False
                self.__Focus.EventsHadDo.hadDoMouseLeftKeyUp = True
                self.__Focus.Events.doMouseLeftKeyUp()
            print('失去焦点元素：', self.__Focus.area, '\n鼠标位置：', MousePos)
            self.__Focus = None

    def doMouseButtonDownEvent(self, MousePos, Button):
        if Button == 1:  # 鼠标右键
            if InElement(MousePos, self.__Focus):
                self.__Focus_onClick = 1
                self.__Focus.Events.doMouseLeftKeyDown()
                self.__Focus.EventsHadDo.hadDoMouseLeftKeyDown = True
                self.__Focus.EventsHadDo.hadDoMouseLeftKeyUp = False

    def doMouseButtonUpEvent(self, MousePos, Button):
        if Button == 1:  # 鼠标右键
            if InElement(MousePos, self.__Focus):
                self.__Focus.Events.doMouseLeftKeyUp()
                self.__Focus.EventsHadDo.hadDoMouseLeftKeyDown = False
                self.__Focus.EventsHadDo.hadDoMouseLeftKeyUp = True
                if self.__Focus_onClick == 1:
                    self.__Focus.Events.doMouseLeftKeyClick()
                    self.__Focus.EventsHadDo.hadDoMouseLeftKeyClick = True
                self.__Focus_onClick = 0


# 新游戏背景故事场景
class NewGame_First_StoryScene(Scene):
    __screen = None
    __ElementsList = None
    __Config = None

    flag_TextDisplayed = False
    flag_BGStory = False
    flag_Img1 = False
    flag_Img2 = False

    # flag 时间
    flag_recordStartTime = False
    start_time = 0
    now_time = 0

    # flag SoundPlay
    flag_BGMPlayed = False
    flag_isSound1Played = False
    flag_isSound2Played = False
    flag_isSound3Played = False
    flag_isSound4Played = False
    flag_isSoundWeakPlayed = False

    flag_VideoPlayed = False

    isReadyToEnd = False
    isEnd = False

    isMusicPlay = False

    MousePos = (0, 0)
    alpha = 0

    # res
    res_Img1 = 'NG_F_SS_1.bmp'
    res_Img2 = 'NG_F_SS_2.bmp'
    Sound_PourWine = 'NG_F_SS_PW.wav'
    Sound_Cup = 'NG_F_SS_C.wav'
    Sound_Drink = 'NG_F_SS_D.wav'
    Sound_Weak = 'NG_F_SS_W.wav'
    Music_BGM = 'NG_F_SS_BGM.wav'
    Video_StartCG = 'FinalSoundCG.mp4'

    res_Sound_PourWine = None
    res_Sound_Cup = None
    res_Sound_Drink = None
    res_Sound_Weak = None
    res_Music_BGM = None
    res_CG_clip = None

    # surface Elements
    __TextShow = None
    __TextList = None
    __DialogueList = None
    __DialogueShow = None
    __Clock = None
    __ImgShow = None
    __counter = 0

    def __init__(self, screen, paramList=None):
        self.__screen = screen
        self.__Config = Config()
        self.__Clock = pygame.time.Clock()

        # 音频
        self.res_Sound_PourWine = pygame.mixer.Sound(gl_SoundPath + self.Sound_PourWine)
        self.res_Sound_PourWine.set_volume(self.__Config.getVolumeSound())

        self.res_Sound_Cup = pygame.mixer.Sound(gl_SoundPath + self.Sound_Cup)
        self.res_Sound_Cup.set_volume(self.__Config.getVolumeSound())

        self.res_Sound_Drink = pygame.mixer.Sound(gl_SoundPath + self.Sound_Drink)
        self.res_Sound_Drink.set_volume(self.__Config.getVolumeSound())

        self.res_Sound_Weak = pygame.mixer.Sound(gl_SoundPath + self.Sound_Weak)
        self.res_Sound_Weak.set_volume(self.__Config.getVolumeSound())

        self.res_Music_BGM = pygame.mixer.Sound(gl_MusicPath + self.Music_BGM)
        self.res_Music_BGM.set_volume(self.__Config.getVolumeBGM())

        # 视频
        self.res_CG_clip = VideoFileClip(gl_VideoPath + self.Video_StartCG).resize((gl_WindowWidth, gl_WindowHeight))

        # 其它元素
        self.__TextList = [const_Text_NewGame_Story_1, const_Text_NewGame_Story_2, const_Text_NewGame_Story_3,
                           const_Text_NewGame_Story_4, const_Text_NewGame_Story_5, const_Text_NewGame_Story_6,
                           const_Text_NewGame_Story_7, const_Text_NewGame_Story_8]
        self.__DialogueList = [const_Text_NewGame__Dialogue_1, const_Text_NewGame__Dialogue_2,
                               const_Text_NewGame__Dialogue_3, const_Text_NewGame__Dialogue_4,
                               const_Text_NewGame__Dialogue_5]

        self.__TextShow = TextElement(pygame.Rect(200, 460, 270, 18), self.__TextList[0], gl_Font_oth, 16,
                                      (255, 255, 255), self.__Config.getTextAntiAlias())
        self.__ImgShow = ImgElement(pygame.Rect(80, 0, 640, 480), gl_ImgPath + self.res_Img1)
        self.__DialogueShow = TextElement(pygame.Rect(0, 500, 430, 18), self.__DialogueList[0], gl_Font_oth, 16,
                                          (255, 255, 255), self.__Config.getTextAntiAlias())

        # 注册元素
        __ElementsList = [self.__TextShow, self.__ImgShow]

    def draw(self):
        if not self.flag_BGStory:
            if self.flag_TextDisplayed:
                self.alpha = 0
                if self.__counter < len(self.__TextList):
                    self.__TextShow.setText(self.__TextList[self.__counter])
                    self.flag_TextDisplayed = False
                else:
                    self.flag_BGStory = True
            else:
                self.alpha += 0.06
            if self.alpha > 255:
                self.flag_TextDisplayed = True
                self.__counter += 1
            self.__TextShow.setAlpha(self.alpha)
            self.__screen.blit(self.__TextShow.res_surface, (
                centeredXPos(self.__screen.get_width(), len(self.__TextShow.Text) * self.__TextShow.Size), 400))
        else:
            if not self.flag_recordStartTime:
                self.start_time = pygame.time.get_ticks()
                self.flag_recordStartTime = True
            self.now_time = pygame.time.get_ticks()
            interval = self.now_time - self.start_time
            if not self.flag_BGMPlayed:
                self.res_Music_BGM.play(loops=-1)
                self.flag_BGMPlayed = True
            if 5000 < interval <= 10000 and not self.flag_Img2:
                self.alpha = 0
                self.__ImgShow.setPath(gl_ImgPath + self.res_Img2)
                self.__DialogueShow.setText(self.__DialogueList[1])
                self.flag_Img2 = True
                if not self.flag_isSoundWeakPlayed:
                    self.res_Sound_Weak.play(loops=0)
                    self.flag_isSoundWeakPlayed = True
            if 10000 < interval <= 15000:
                if not self.flag_isSound1Played:
                    self.res_Sound_Cup.play(loops=0)
                    self.flag_isSound1Played = True
                self.__DialogueShow.setText(self.__DialogueList[2])
            if 20000 < interval <= 25000:
                if not self.flag_isSound2Played:
                    self.res_Sound_PourWine.play(loops=0)
                    self.flag_isSound2Played = True
                self.__DialogueShow.setText(self.__DialogueList[3])
            if 25000 < interval <= 30000:
                if not self.flag_isSound3Played:
                    self.res_Sound_Drink.play(loops=0)
                    self.flag_isSound3Played = True
                self.__DialogueShow.setText(self.__DialogueList[4])
            if 30000 < interval <= 35000:
                if not self.flag_isSound4Played:
                    self.res_Sound_Cup.play(loops=0)
                    self.flag_isSound4Played = True
            if 30000 < interval <= 33000:
                self.alpha -= 6
                self.__ImgShow.setAlpha(self.alpha)
                self.__DialogueShow.setAlpha(self.alpha)
            if 33000 < interval <= 50000:
                if not self.flag_VideoPlayed:
                    self.res_CG_clip.preview()
                    self.flag_VideoPlayed = True
            self.alpha += 2
            if self.alpha >= 255:
                self.__screen.blit(self.__DialogueShow.res_surface, (
                    centeredXPos(self.__screen.get_width(), len(self.__DialogueShow.Text) * self.__DialogueShow.Size),
                    self.__DialogueShow.area.top))
                self.alpha = 255
            self.__ImgShow.setAlpha(self.alpha)
            self.__screen.blit(self.__ImgShow.res_surface, (self.__ImgShow.area.left, self.__ImgShow.area.top))


def ChePos(e, isDown):
    if isDown:
        e.area.top += 1
        e.area.left += 1
    else:
        e.area.top -= 1
        e.area.left -= 1


class OptionScene(Scene):
    __screen = None
    __Config = None
    __Focus = None
    __Focus_onClick = 0
    __ElementsMap = None

    MousePos = (0, 0)
    isReadyToEnd = False
    isEnd = False
    __flag_isEnter = False

    __alpha = 0

    __Clock = None
    __flag_recordStartTime = False
    __start_time = 0
    __now_time = 0

    res_Img_BG_Name = 'OPT_BG.bmp'
    res_Sound_Choose_Name = 'OPT_C.wav'
    res_Img_BG = None
    res_Sound_Choose = None
    res_UI_RightButton = 'OPT_BR.png'
    res_UI_LeftButton = 'OPT_BL.png'

    __E_BGBlankR = None
    __E_BGBlankL1 = None
    __E_BGBlankL2 = None
    __E_BGBlankL3 = None
    __E_BGBlankLApply = None
    __E_BGBlankLRet = None

    __E_Text_Apply = None
    __E_Text_Ret = None

    __E_Text_Draw = None
    __E_Text_AntiAlias = None
    __E_Text_AA_Val = None
    __E_UI_AA_LeftButton = None
    __E_UI_AA_RightButton = None

    __E_Text_Wave = None
    __E_Text_BGMVolume = None
    __E_Text_BGM_Val = None
    __E_UI_BGM_LeftButton = None
    __E_UI_BGM_RightButton = None
    __E_Text_SoundVolume = None
    __E_Text_Sou_Val = None
    __E_UI_Sou_LeftButton = None
    __E_UI_Sou_RightButton = None
    __E_Text_Licence = None
    __E_Img_Licence = None

    __KV_AA = None
    __KV_WAVE = None

    def __init__(self, screen, paramList=None):
        if paramList is not None:
            self.__flag_isEnter = paramList[0]

        # 注册与该场景相关的场景
        from clazz.AppConfig import registerScene
        registerScene(SCREEN_OPT_APPLY, OptionScene, [True])

        self.__screen = screen
        self.__Config = Config()
        self.__Clock = pygame.time.Clock()
        self.__KV_AA = {}
        self.__KV_WAVE = {}
        self.__ElementsMap = {}

        if self.__Config.getTextAntiAlias():
            self.__KV_AA['key'] = '开'
            self.__KV_AA['val'] = '1'
        else:
            self.__KV_AA['key'] = '关'
            self.__KV_AA['val'] = '0'

        self.res_Sound_Choose = pygame.mixer.Sound(gl_SoundPath + self.res_Sound_Choose_Name)
        self.res_Sound_Choose.set_volume(self.__Config.getVolumeSound())

        self.res_Img_BG = pygame.image.load(gl_ImgPath + self.res_Img_BG_Name)

        self.__E_BGBlankL1 = OptButtonElement(pygame.Rect(40, 60, 200, 40), (255, 255, 255, 100))
        self.__E_BGBlankL2 = OptButtonElement(pygame.Rect(40, 110, 200, 40), (255, 255, 255, 100))
        self.__E_BGBlankL3 = OptButtonElement(pygame.Rect(40, 160, 200, 40), (255, 255, 255, 100))
        self.__E_BGBlankLRet = OptButtonElement(pygame.Rect(50, 520, 80, 40), (255, 255, 255, 100))
        self.__E_BGBlankLApply = OptButtonElement(pygame.Rect(150, 520, 80, 40), (255, 255, 255, 100))
        self.__E_BGBlankR = TitleConstElement(pygame.Rect(260, 60, 510, 500),
                                              blankSurface((510, 500), (255, 255, 255, 100)))
        self.__E_Text_Apply = TextElement(pygame.Rect(centeredXPos(80, 40, 150), centeredYPos(40, 20, 520), 120, 20),
                                          '应用', gl_Font_opt, 20, (0, 0, 0), self.__Config.getTextAntiAlias())
        self.__E_Text_Ret = TextElement(pygame.Rect(centeredXPos(80, 40, 50), centeredYPos(40, 20, 520), 120, 20),
                                        '返回', gl_Font_opt, 20, (0, 0, 0), self.__Config.getTextAntiAlias())

        self.__E_Text_Draw = TextElement(pygame.Rect(centeredXPos(200, 80, 40), centeredYPos(40, 20, 60), 80, 20),
                                         '画面设置', gl_Font_opt, 20, (0, 0, 0), self.__Config.getTextAntiAlias())
        self.__E_Text_AntiAlias = TextElement(pygame.Rect(270, 70, 120, 20), '抗锯齿：', gl_Font_opt, 18, (0, 0, 0),
                                              self.__Config.getTextAntiAlias())

        self.__E_Text_AA_Val = TextElement(pygame.Rect(670, 70, 20, 20), self.__KV_AA['key'], gl_Font_opt, 18,
                                           (0, 0, 0),
                                           self.__Config.getTextAntiAlias())
        self.__E_UI_AA_RightButton = OptUIElement(pygame.Rect(700, 70, 20, 20), gl_UIPath + self.res_UI_RightButton)
        self.__E_UI_AA_LeftButton = OptUIElement(pygame.Rect(640, 70, 20, 20), gl_UIPath + self.res_UI_LeftButton)

        self.__E_Text_Wave = TextElement(pygame.Rect(centeredXPos(200, 80, 40), centeredYPos(40, 20, 110), 80, 20),
                                         '声音设置', gl_Font_opt, 20, (0, 0, 0), self.__Config.getTextAntiAlias())
        self.__E_Text_BGMVolume = TextElement(pygame.Rect(270, 70, 120, 20), '音乐音量：', gl_Font_opt, 18, (0, 0, 0),
                                              self.__Config.getTextAntiAlias())
        self.__E_Text_BGM_Val = TextElement(pygame.Rect(660, 70, 30, 20), str(self.__Config.VolumeBGM),
                                            gl_Font_opt, 18, (0, 0, 0), self.__Config.getTextAntiAlias())
        self.__E_UI_BGM_RightButton = OptUIElement(pygame.Rect(700, 70, 20, 20), gl_UIPath + self.res_UI_RightButton)
        self.__E_UI_BGM_LeftButton = OptUIElement(pygame.Rect(630, 70, 20, 20), gl_UIPath + self.res_UI_LeftButton)
        self.__E_Text_SoundVolume = TextElement(pygame.Rect(270, 100, 120, 20), '音效音量：', gl_Font_opt, 18, (0, 0, 0),
                                                self.__Config.getTextAntiAlias())
        self.__E_Text_Sou_Val = TextElement(pygame.Rect(660, 100, 30, 20), str(self.__Config.VolumeSound),
                                            gl_Font_opt, 18, (0, 0, 0), self.__Config.getTextAntiAlias())
        self.__E_UI_Sou_RightButton = OptUIElement(pygame.Rect(700, 100, 20, 20), gl_UIPath + self.res_UI_RightButton)
        self.__E_UI_Sou_LeftButton = OptUIElement(pygame.Rect(630, 100, 20, 20), gl_UIPath + self.res_UI_LeftButton)

        self.__E_Text_Licence = TextElement(
            pygame.Rect(centeredXPos(200, 120, 40), centeredYPos(40, 20, 160), 120, 20), '开源软件许可', gl_Font_opt, 20,
            (0, 0, 0), self.__Config.getTextAntiAlias())
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
                                                  lambda: self.__retSignalIsReadyToEnd(SCREEN_OPT_APPLY), 1)
        self.__E_BGBlankLApply.Events.appendEvent(ioEvent3Enum.mouseLeftKeyClick, lambda: self.__updConfig(), 2)

        # 返回按钮绑定事件
        self.__E_BGBlankLRet.Events.appendEvent(ioEvent3Enum.mouseLeftKeyDown, lambda: ChePos(self.__E_Text_Ret, True),
                                                1)
        self.__E_BGBlankLRet.Events.appendEvent(ioEvent3Enum.mouseLeftKeyUp, lambda: ChePos(self.__E_Text_Ret, False),
                                                1)
        self.__E_BGBlankLRet.Events.appendEvent(ioEvent3Enum.mouseLeftKeyClick,
                                                lambda: self.__retSignalIsReadyToEnd(SCREEN_TITLE), 1)

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
        interval = self.__start_time - self.__now_time

        blitAlpha(self.__screen, self.res_Img_BG, (0, 0), self.__alpha)

        if not self.__flag_isEnter and not self.isReadyToEnd:
            self.__alpha += 4
            if self.__alpha >= 255:
                self.__alpha = 255
                self.__flag_isEnter = True
        elif self.__flag_isEnter and not self.isReadyToEnd:
            self.__alpha = 255
            for e in self.__ElementsMap['Draw']:
                e.draw(self.__screen)
        if self.isReadyToEnd:
            self.isEnd = True

    def doMouseMotion(self, MousePos, MouseRel, Buttons):
        if not eq(Buttons, (0, 0, 0)) or self.__ElementsMap['Interact'] is None:
            return
        if self.__Focus is None and len(self.__ElementsMap['Interact']):
            for e in self.__ElementsMap['Interact']:
                if InElement(MousePos, e) and e.EventsHadDo.hadDoMouseOut:
                    self.__Focus = e
                    self.__Focus.Events.doMouseIn()
                    print('确定焦点元素：', self.__Focus.area, '\n鼠标位置：', MousePos)
        if not InElement(MousePos, self.__Focus) and self.__Focus is not None:
            self.__Focus.Events.doMouseOut()
            if self.__Focus.EventsHadDo.hadDoMouseLeftKeyDown:
                self.__Focus.Events.doMouseLeftKeyUp()
                self.__Focus.EventsHadDo.hadDoMouseLeftKeyDown = False
                self.__Focus.EventsHadDo.hadDoMouseLeftKeyUp = True
            print('失去焦点元素：', self.__Focus.area, '\n鼠标位置：', MousePos)
            self.__Focus = None

    def doMouseButtonDownEvent(self, MousePos, Button):
        if Button == 1:  # 鼠标右键
            if InElement(MousePos, self.__Focus):
                self.__Focus_onClick = 1
                self.__Focus.Events.doMouseLeftKeyDown()
                self.__Focus.EventsHadDo.hadDoMouseLeftKeyDown = True
                self.__Focus.EventsHadDo.hadDoMouseLeftKeyUp = False

    def doMouseButtonUpEvent(self, MousePos, Button):
        if Button == 1:  # 鼠标右键
            if InElement(MousePos, self.__Focus):
                self.__Focus.Events.doMouseLeftKeyUp()
                self.__Focus.EventsHadDo.hadDoMouseLeftKeyDown = False
                self.__Focus.EventsHadDo.hadDoMouseLeftKeyUp = True
                if self.__Focus_onClick == 1:
                    self.__Focus.Events.doMouseLeftKeyClick()
                    self.__Focus.EventsHadDo.hadDoMouseLeftKeyClick = True
                self.__Focus_onClick = 0


class Continue_Scene(Scene):
    __screen = None
    __ElementsList = None

    isReadyToEnd = False
    isEnd = False
