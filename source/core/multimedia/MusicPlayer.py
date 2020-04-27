import wave
import numpy as np


class musicPlayer:
    def __init__(self, ):
        self.__pathMap = {}
        self.__activeMap = {}

    def add(self, name, path):
        self.__pathMap[name] = path

    def addAll(self, lis):
        for e in lis:
            self.__pathMap[e[0]] = e[1]

    def play(self, name):
        pass

    def active(self, name):
        f = wave.open(self.__pathMap[name], 'rb')
        self.__activeMap[name] = f

    def close(self, name):
        self.__activeMap[name].close()

    def getMsg(self, name, step):
        m = self.__activeMap[name]
        # params = m.getparams()
        # nchannels, sampwidth, framerate, nframes = params[:4]
        # print(framerate)
        str_data = m.readframes(step)  # 80000是前10秒
        # print(str_data)
        wave_data = np.frombuffer(str_data, dtype=np.short)
        wave_data.shape = -1, 2
        wave_data = wave_data.T
        return wave_data[0]
        # time = np.arange(0, 80000) * (1.0 / 44100)

        # pl.subplot(211)
        # pl.plot(time, wave_data[0])
        # pl.subplot(212)
        # pl.plot(time, wave_data[1], c="g")
        # pl.xlabel("time (seconds)")
        # pl.show()


# player = musicPlayer()
# player.add('0', 'F:/练习/PyCharm/PygameTest/resource/Test/雪之华.wav')
# player.active('0')
# player.getMsg('0')
# player.close('0')
