import threading


class core_thread(threading.Thread):
    def __init__(self, threadID, name, counter, fuc):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.fuc = fuc

    def run(self):
        print(self.name)
        self.fuc()
