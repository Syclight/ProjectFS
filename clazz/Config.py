from clazz.Const import GLC_INI_NAME, GLC_INI_SECTION_DRAW, GLC_INI_PARAM_ANTIALIAS, GLC_INI_SECTION_WAVE, \
    GLC_INI_PARAM_BGMVOLUME, GLC_INI_PARAM_SOUNDVOLUME
from clazz.ToolsFuc import readINIBool, readINIFloat


class Config:
    TextAntiAlias = None
    VolumeBGM = None
    VolumeSound = None

    def __init__(self):
        pass

    def readConfig(self):
        self.TextAntiAlias = readINIBool(GLC_INI_NAME, GLC_INI_SECTION_DRAW, GLC_INI_PARAM_ANTIALIAS)
        self.VolumeBGM = readINIFloat(GLC_INI_NAME, GLC_INI_SECTION_WAVE, GLC_INI_PARAM_BGMVOLUME)
        self.VolumeSound = readINIFloat(GLC_INI_NAME, GLC_INI_SECTION_WAVE, GLC_INI_PARAM_SOUNDVOLUME)

    def getTextAntiAlias(self):
        return self.TextAntiAlias

    def getVolumeBGM(self):
        return self.VolumeBGM * 0.1

    def getVolumeSound(self):
        return self.VolumeSound * 0.1
