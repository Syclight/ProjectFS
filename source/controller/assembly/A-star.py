#  启发函数
def heuristic(a, b):
    return abs(a.i - b.i) + abs(a.j - b.j)


class Spot:
    def __init__(self, i, j):
        self.i = i  # 该位置X坐标
        self.j = j  # 该位置Y坐标
        self.g = 0  # 从起点到当前位置的距离
        self.h = 0  # 从终点到当前位置距离，需要计算
        self.f = 0  # g + h这是最短路径的依据，g + h最小，则说明该点越在最短路径上
        self.neighbors = []  # 邻居集合，即子节点
        self.previous = None  # 父节点，即该位置的上一个位置
        self.wall = False  # 是否是无法穿越的位置

    def addNeighbors(self, cols, rows, grid):
        i, j = self.i, self.j
        if i < cols - 1:
            self.neighbors.append(grid[i + 1][j])
        if i > 0:
            self.neighbors.append(grid[i - 1][j])
        if j < rows - 1:
            self.neighbors.append(grid[i][j + 1])
        if j > 0:
            self.neighbors.append(grid[i][j - 1])
        if i > 0 and j > 0:
            self.neighbors.append(grid[i - 1][j - 1])
        if i < cols - 1 and j > 0:
            self.neighbors.append(grid[i + 1][j - 1])
        if i > 0 and j < rows - 1:
            self.neighbors.append(grid[i - 1][j + 1])
        if i < cols - 1 and j < rows - 1:
            self.neighbors.append(grid[i + 1][j + 1])


class AStartArea:
    def __init__(self, rect, cols, rows, start=None, end=None):
        self.__grid = []
        self.rect = rect
        self.cols, self.rows = cols, rows
        self.unit_w, self.unit_h = self.rect.w / self.cols, self.rect.w / self.rows
        self.__openSet, self.__closeSet = [], []
        self.start, self.end = None, None
        self.__initArea()
        if start is not None:
            self.start = self.__grid[start[0]][start[1]]
            self.__openSet.append(self.start)
        if end is not None:
            self.end = self.__grid[end[0]][end[1]]
        self.__done = False
        self.__noSolution = False
        self.__resList = []
        self.__wallsMap = []

    def __initArea(self):
        for i in range(0, self.cols):
            self.__grid.append([])

        for i in range(0, self.cols):
            for j in range(0, self.rows):
                self.__grid[i].append(Spot(i, j))

        for i in range(0, self.cols):
            for j in range(0, self.rows):
                self.__grid[i][j].addNeighbors(self.cols, self.rows, self.__grid)

    def addObstacle(self, x, y):
        if self.start is not None or self.end is not None:
            if self.start.i == x and self.start.j == y or self.end.i == x and self.end.j == y:
                raise Exception('Obstacle pos ({}, {}) should not be startPos or endPos'.format(x, y))
        self.__grid[x][y].wall = True
        self.__wallsMap.append((x, y))

    def addObstacles(self, pos_list):
        for x, y in pos_list:
            self.addObstacle(x, y)

    def removeObstacle(self, x, y):
        self.__grid[x][y].wall = False
        self.__wallsMap.remove((x, y))

    def removeObstacles(self, pos_list):
        for x, y in pos_list:
            self.removeObstacle(x, y)

    def removeAllObstacles(self):
        for x, y in self.__wallsMap:
            self.__grid[x][y].wall = False
        self.__wallsMap.clear()

    def getObstaclesList(self):
        return self.__wallsMap

    def refresh(self):
        tempWall = self.__wallsMap
        self.__init__(self.rect, self.cols, self.rows)
        self.__wallsMap = tempWall
        for x, y in self.__wallsMap:
            self.__grid[x][y].wall = True

    def setStart(self, start):
        x, y = start[0], start[1]
        if self.__grid[x][y].wall:
            raise Exception('There are obstacle at pos ({}, {})'.format(x, y))
        self.start = self.__grid[x][y]
        self.__openSet.append(self.start)

    def setEnd(self, end):
        x, y = end[0], end[1]
        if self.__grid[x][y].wall:
            raise Exception('There are obstacle at pos ({}, {})'.format(x, y))
        self.end = self.__grid[x][y]

    def run(self):
        while not self.__done:
            if len(self.__openSet) > 0:
                winner = 0
                for i in range(0, len(self.__openSet)):
                    if self.__openSet[i].f < self.__openSet[winner].f:
                        winner = i

                current = self.__openSet[winner]

                if current == self.end:
                    self.__done = True

                if not self.__done:
                    self.__openSet.remove(current)
                    self.__closeSet.append(current)

                    neighbors = current.neighbors
                    for n in neighbors:
                        if n not in self.__closeSet and not n.wall:
                            tempG = current.g + 1
                            newPath = False
                            if n in self.__openSet:
                                if tempG < n.g:
                                    n.g = tempG
                                    newPath = True
                            else:
                                n.g = tempG
                                newPath = True
                                self.__openSet.append(n)
                            if newPath:
                                # 这里的启发函数是自定义的，用于测定启发点到当前点的距离(也可以理解成消耗资源量)
                                n.h = heuristic(n, self.end)
                                n.f = n.g + n.h
                                n.previous = current
            else:
                self.__noSolution = True
                return False

            if not self.__done:
                self.__resList.clear()
                temp = current
                self.__resList.append((temp.i, temp.j))
                while temp is not None and temp.previous:
                    self.__resList.append((temp.previous.i, temp.previous.j))
                    temp = temp.previous
            else:
                self.__resList.reverse()
                self.__resList.append((self.end.i, self.end.j))
                return self.__resList


# area = AStartArea(Rectangle(0, 0, 500, 500), 10, 10)
# area.addObstacle(4, 4)
# area.addObstacles([(5, 5), (3, 3), (6, 5)])
# area.setStart((0, 0))
# area.setEnd((9, 9))
# print(area.run())
# area.refresh()
# area.removeAllObstacles()
# area.setStart((0, 0))
# area.setEnd((9, 9))
# print(area.run())
