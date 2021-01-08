class Timer:
    def __init__(self):
        self.__secondsPerCount = 0.0
        self.__deltaTime = -1.0

        self.__baseTime = 0
        self.__pausedTime = 0
        self.__stopTime = 0
        self.__prevTime = 0
        self.__currTime = 0

        self.__stopped = False

        self.countsPerSec = 0


