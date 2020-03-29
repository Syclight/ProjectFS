from source.const.Const import GLC_INI_NAME, GLC_INI_SECTION_DRAW, GLC_INI_PARAM_ANTIALIAS, GLC_INI_SECTION_WAVE, \
    GLC_INI_PARAM_BGMVOLUME, GLC_INI_PARAM_SOUNDVOLUME, GLC_INI_PARAM_FRAMERATE
from source.util.ToolsFuc import readINIBool, readINIFloat, readINIInt


class Config:
    def __init__(self):
        self.TextAntiAlias = None
        self.VolumeBGM = None
        self.VolumeSound = None
        self.FrameRate = None
        self.path = GLC_INI_NAME

    def readConfig(self):
        self.TextAntiAlias = readINIBool(self.path, GLC_INI_SECTION_DRAW, GLC_INI_PARAM_ANTIALIAS)
        self.VolumeBGM = readINIFloat(self.path, GLC_INI_SECTION_WAVE, GLC_INI_PARAM_BGMVOLUME)
        self.VolumeSound = readINIFloat(self.path, GLC_INI_SECTION_WAVE, GLC_INI_PARAM_SOUNDVOLUME)
        self.FrameRate = readINIInt(self.path, GLC_INI_SECTION_DRAW, GLC_INI_PARAM_FRAMERATE)

    def getTextAntiAlias(self):
        return self.TextAntiAlias

    def getVolumeBGM(self):
        return self.VolumeBGM * 0.1

    def getVolumeSound(self):
        return self.VolumeSound * 0.1

    def getFrameRate(self):
        if self.FrameRate == 0:
            return 0
        if self.FrameRate < 30:
            return 30
        if self.FrameRate > 120:
            return 120
        return self.FrameRate
