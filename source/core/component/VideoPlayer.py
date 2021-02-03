from moviepy.audio.fx.volumex import volumex
from moviepy.editor import *


class VideoPlay:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
            cls.__clipDict = dict()
        return cls._instance

    def __init__(self):
        pass

    def add(self, strId, path, size=None, volume=None):
        clip = VideoFileClip(path)
        if size:
            clip.resize(size)
        if volume:
            clip = volumex(clip, volume)
        self.__clipDict[strId] = clip

    def preview(self, strId, fps=15, isAudio=True):
        self.__clipDict[strId].preview(fps=fps, audio=isAudio)

    def show(self, strId):
        self.__clipDict[strId].show()
