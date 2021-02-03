class MiniQueue:
    def __init__(self, capacity):
        self.__capacity = capacity
        self.__ptr = -1
        self.__list = [None] * self.__capacity

    def __str__(self):
        return self.__list.__str__()

    def __len__(self):
        return self.__ptr + 1

    def content(self):
        return self.__list

    def size(self):
        return self.__capacity

    def push(self, e):
        self.__ptr += 1
        if self.__ptr > self.__capacity - 1:
            self.pop()
        self.__list[self.__ptr] = e

    def pop(self):
        e = self.__list[0]
        for i in range(0, self.__capacity - 1):
            self.__list[i] = self.__list[i + 1]
        self.__ptr -= 1
        return e
