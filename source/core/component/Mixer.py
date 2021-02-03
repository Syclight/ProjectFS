import pygame


class Mixer:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
            cls.__soundDict = dict()
            cls.__channelDict = dict()
            cls.__musicDict = dict()
            pygame.mixer.init()
        return cls._instance

    def quit(self):
        self.__soundDict.clear()
        self.__musicDict.clear()
        self.__channelDict.clear()
        pygame.mixer.quit()

    def __init__(self):
        pass

    def addSound(self, strId, path):
        self.__soundDict[strId] = pygame.mixer.Sound(path)

    def playSound(self, strId, loops=0, maxTime=0, fadeMs=0):
        self.__soundDict[strId].play(loops, maxTime, fadeMs)

    def setVolSound(self, strId, vol):
        self.__soundDict[strId].set_volume(vol)

    def pauseSound(self, strId):
        self.__soundDict[strId].puse()

    def unpauseSound(self, strId):
        self.__soundDict[strId].unpause()

    def stopSound(self, strId):
        self.__soundDict[strId].stop()

    def createChannel(self, strId, channelId=None):
        if channelId:
            self.__channelDict[strId] = pygame.mixer.Channel(channelId)
        else:
            self.__channelDict[strId] = pygame.mixer.find_channel()

    def setVolChannel(self, strId, vol):
        self.__channelDict[strId].set_volume(vol)

    def playSoundByChannel(self, channelStrId, soundStrId, loops=0, maxTime=0, fadeMs=0):
        self.__channelDict[channelStrId].play(self.__soundDict[soundStrId], loops, maxTime, fadeMs)

    @staticmethod
    def numOfChannel(self):
        return pygame.mixer.get_num_channels()

    def addMusic(self, strId, path):
        self.__musicDict[strId] = path

    def loadMusic(self, strId):
        pygame.mixer.music.load(self.__musicDict[strId])

    @staticmethod
    def playMusic(self, loops=0, start=0.0):
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(loops, start)

    @staticmethod
    def replayMusic(self):
        pygame.mixer.music.rewind()

    @staticmethod
    def pauseMusic(self):
        pygame.mixer.music.pause()

    @staticmethod
    def stopMusic(self):
        pygame.mixer.music.stop()

    @staticmethod
    def restoreMusic(self):
        pygame.mixer.music.unpause()

    @staticmethod
    def fadeoutMusic(self, time):
        pygame.mixer.music.fadeout(time)

    @staticmethod
    def setVolumeMusic(self, val):
        pygame.mixer.music.set_volume(val)
