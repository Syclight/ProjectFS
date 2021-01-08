import pygame

from source.core.assembly.IOEvent import ioEvent3Enum
from source.core.math.Vector import vec3, vec2
from source.util.ToolsFuc import createSurfaceFromFile, ex_toRectTangle, centeredXPos, blankSurface, centeredYPos, \
    clipResImg
from source.view.baseClazz.Scene import Scene
from source.view.baseClazz.Sprite import Sprite
from source.view.element.Elements import ImgElement

g_resPath = 'source/view/origin/res/'


class GearSprite(Sprite):
    def __init__(self, image, rect):
        super().__init__(image, rect)
        self._image = self.image
        self.rotate = 0
        self.beginTime = 0
        self.nowTime = 0

    def update(self, *args):
        if self.beginTime == 0:
            self.beginTime = args[0]
        self.nowTime = args[0]
        interval = self.nowTime - self.beginTime
        if interval > 10:
            self.rotate += 0.5
            self.beginTime = 0
        self.image = pygame.transform.rotate(self._image, self.rotate)
        self.rect = self.image.get_rect(center=self.rect.center)


class AirShipSprite(Sprite):
    def __init__(self, image, rect):
        super().__init__(image, rect)
        self._image = self.image
        self.vel = 1
        self.max_rectY = self.rect.y + 10
        self.min_rectY = self.rect.y - 10
        self.zIndex = 15

        self.beginTime = 0
        self.nowTime = 0

    def update(self, *args):
        if self.beginTime == 0:
            self.beginTime = args[0]
        self.nowTime = args[0]
        interval = self.nowTime - self.beginTime
        if interval > 100:
            self.rect.y += self.vel
            if self.rect.y >= self.max_rectY or self.rect.y <= self.min_rectY:
                self.vel = -self.vel
            self.beginTime = 0


class TravellerSprite(Sprite):
    def __init__(self, *args):
        super().__init__(*args)
        self.scale = 0.8
        self.__initImg = self.image
        self.__initRect = self.rect
        self.keyPoint = (
            vec3(self.rect.x, self.rect.y, 225), vec3(625, 642, 240), vec3(680, 620, 180), vec3(740, 610, 100),
            vec3(-999, -999, 0))
        self.zIndex = 21
        self.i = 0
        self.beginTime = 0
        self.nowTime = 0

    def update(self, *args):
        if self.beginTime == 0:
            self.beginTime = args[0]
        self.nowTime = args[0]
        interval = self.nowTime - self.beginTime
        if interval > 10000:
            self.i += 1
            if self.i == 5:
                self.i = -1
                self.setRect(self.__initRect)
                self.image = self.__initImg
                self.image.set_alpha(225)
            else:
                temp_scale = 1 if self.i == 0 else self.scale
                self.setRect((self.keyPoint[self.i].x, self.keyPoint[self.i].y, self.rect.w * temp_scale,
                              self.rect.h * temp_scale))
                self.image.set_alpha(self.keyPoint[self.i].z)
                self.beginTime = 0


class OptionSprite(Sprite):
    def __init__(self, *args, typeNum=None):
        super(OptionSprite, self).__init__(*args)
        self.type = typeNum
        self.__setup()

    def __setup(self):
        temp = pygame.Surface((self.rect.w, self.rect.h)).convert()
        if self.type == 0:
            temp.blit(self.image, (-self.rect.y, -self.rect.x))
        self.image = temp


class ReflectElement(ImgElement):
    def __init__(self, *args):
        super(ReflectElement, self).__init__(*args)
        self.vel = 1
        self.max_rectY = self.area.y + 20
        self.min_rectY = self.area.y - 20
        self.zIndex = 19

        self.beginTime = 0
        self.nowTime = 0

    def update(self, time):
        if self.beginTime == 0:
            self.beginTime = time
        self.nowTime = time
        interval = self.nowTime - self.beginTime
        if interval > 100:
            self.area.y += self.vel
            if self.area.y >= self.max_rectY or self.area.y <= self.min_rectY:
                self.vel = -self.vel
            self.beginTime = 0


class MaskElement(ImgElement):
    def __init__(self, *args):
        super(MaskElement, self).__init__(*args)
        self.zIndex = 1000
        self.a = 225

        self.__beginTime = 0
        self.__nowTime = 0

    def update(self, time):
        if self.__beginTime == 0:
            self.__beginTime = time
        self.__nowTime = time
        if self.a >= 0 or self.__nowTime - self.__beginTime > 400:
            self.a -= 8
            if self.a <= 0:
                self.a = 0
                self.active = False
                self.visual = False
                self.zIndex = -999
            self.setAlpha(self.a)
            self.__beginTime = 0


class OriginLogo(Scene):
    def __init__(self, *args):
        super(OriginLogo, self).__init__(*args)
        # 注册与该场景相关的场景
        from source.config.AppConfig import registerScene
        registerScene(101, OriginTitle)
        self.nextSceneNum = 101
        self.resPath = {'logoText1': 'logo.jpg', 'logoText2': 'logo2.jpg'}
        self.bgSurface = blankSurface((self.width, self.height))
        self.__ele_Logo1 = ImgElement((centeredXPos(self.width, 211), centeredYPos(self.height, 27) - 20, 211, 27),
                                      g_resPath + self.resPath['logoText1'])
        self.__ele_Logo2 = ImgElement((centeredXPos(self.width, 444), centeredYPos(self.height, 35) - 20, 444, 35),
                                      g_resPath + self.resPath['logoText2'])
        self.__ele_Logo2.visual = False
        self.__beginTime = 0
        self.__nextTime = 0
        self.__nowTime = 0

    def setup(self):
        self.caption = 'FinialSound:Origin 终曲：起源 v1.0.0'
        self.render.open()
        self.render.add(self.__ele_Logo1, self.__ele_Logo2)
        self.render.close()

    def doClockEvent(self, NowClock):
        if self.__beginTime == 0:
            self.__beginTime = NowClock
        self.__nowTime = NowClock
        if self.__nowTime - self.__beginTime > 2000:
            if self.__ele_Logo1.visual:
                self.__ele_Logo1.visual = False
                self.__ele_Logo2.visual = True
                self.__beginTime = 0
            else:
                self.isEnd = True


class OriginTitle(Scene):
    def __init__(self, *args):
        super(OriginTitle, self).__init__(*args)
        self.__tempSurf = None
        self.resPath = {'bg_back': 'bg_back.jpg', 'bg_gear': 'bg_gear.png', 'bg_town': 'bg_town.png',
                        'bg_airship': 'bg_airship.png', 'bgm': 'bg_BGM.wav', 'bg_title': 'bg_title.png',
                        'bg_options': 'bg_options.png', 'bg_rive': 'bg_rive.png', 'bg_reflect': 'bg_reflect.jpg',
                        'bg_traveller': 'bg_traveller.png', 'bg_bridge': 'bg_bridge.png',
                        'bg_copyright': 'bg_copyright.png', 'bg_pen': 'bg_pen.png', 'bg_penBk': 'bg_pen_bk.png'}
        # self.__spr_mouse = Sprite()
        # self.__spr_option1 = OptionSprite()
        self.__ele_mask = MaskElement((0, 0, self.width, self.height))

        self.__bgGear_InitImg = pygame.image.load(g_resPath + self.resPath['bg_gear'])
        self.__spr_bgGear = GearSprite(self.__bgGear_InitImg, pygame.Rect(300, 100, 528, 528))
        self.__spr_bgGear.zIndex = 10
        self.__spr_airship0 = AirShipSprite(pygame.image.load(g_resPath + self.resPath['bg_airship']),
                                            pygame.Rect(250, 45, 166, 153))
        self.__spr_airship1 = AirShipSprite(pygame.image.load(g_resPath + self.resPath['bg_airship']),
                                            pygame.Rect(100, 70, 83, 77))
        self.__spr_airship1.vel = 2
        self.__spr_airship2 = AirShipSprite(pygame.image.load(g_resPath + self.resPath['bg_airship']),
                                            pygame.Rect(180, 200, 33, 31))
        self.__spr_airship2.vel = -1
        self.__spr_traveller = TravellerSprite(
            pygame.image.load(g_resPath + self.resPath['bg_traveller']).convert_alpha(), pygame.Rect(540, 660, 93, 47))
        self.__ele_bgTown = ImgElement((0, 0, 1280, 720), g_resPath + self.resPath['bg_town'])
        self.__ele_bgTown.zIndex = 20
        self.__ele_bgBridge = ImgElement((612, self.height - 173, 247, 173), g_resPath + self.resPath['bg_bridge'])
        self.__ele_bgBridge.zIndex = 30
        self.__ele_bgRive = ImgElement((0, 650, 1280, 70), g_resPath + self.resPath['bg_rive'])
        self.__ele_bgRive.zIndex = 18
        self.__ele_bgReflect = ReflectElement((-250, 570, 1280, 184), g_resPath + self.resPath['bg_reflect'], 80)
        self.__ele_bgTitle = ImgElement((centeredXPos(1280, 450) + 40, 240, 450, 80),
                                        g_resPath + self.resPath['bg_title'])
        self.__ele_bgTitle.zIndex = 100
        self.__ele_bgOptions = ImgElement((centeredXPos(self.width, 88), 320, 88, 109),
                                          g_resPath + self.resPath['bg_options'])
        self.__ele_bgOptions.zIndex = 100
        self.__ele_bgPen = ImgElement((self.__ele_bgOptions.area.x - 10, self.__ele_bgOptions.area.y + 4, 12, 21),
                                      g_resPath + self.resPath['bg_pen'])
        self.__ele_bgPen.zIndex = 99
        self.__ele_bgPenBk = ImgElement((self.__ele_bgPen.area.x + 6, self.__ele_bgPen.area.y + 14, 102, 5),
                                        g_resPath + self.resPath['bg_penBk'])
        self.__ele_bgPenBk.zIndex = 98
        self.__ele_bgCopyright = ImgElement((2, self.height - 22, 274, 18), g_resPath + self.resPath['bg_copyright'])
        self.__ele_bgCopyright.zIndex = 999

        self.rot = 0
        self.__wave_bgm = pygame.mixer.Sound(g_resPath + self.resPath['bgm'])

    def setup(self):
        self.caption = 'FinialSound:Origin 终曲：起源 v1.0.0'
        # self.useDefaultDraw = False
        self.bgSurface = createSurfaceFromFile(g_resPath + self.resPath['bg_back'])
        self.render.open()
        self.render.add(self.__spr_bgGear, self.__ele_bgTown, self.__spr_airship0,
                        self.__spr_airship1, self.__spr_airship2, self.__ele_bgTitle,
                        self.__ele_bgRive, self.__ele_bgReflect, self.__spr_traveller,
                        self.__ele_bgBridge, self.__ele_bgCopyright, self.__ele_mask,
                        self.__ele_bgOptions, self.__ele_bgPen, self.__ele_bgPenBk)
        self.render.close()
        self.__wave_bgm.play(loops=-1)

    # def draw(self):
    #     self.render.render(self.screen)

    def doClockEvent(self, NowClock):
        self.__ele_mask.update(NowClock)
        self.__spr_bgGear.update(NowClock)
        self.__spr_airship0.update(NowClock)
        self.__spr_airship1.update(NowClock)
        self.__spr_airship2.update(NowClock)
        self.__spr_traveller.update(NowClock)
        self.__ele_bgReflect.update(NowClock)
