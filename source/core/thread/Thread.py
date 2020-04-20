import threading


class Thread(threading.Thread):
    def __init__(self, threadID, name, counter, fuc):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.fuc = fuc

    def run(self):
        self.fuc()
