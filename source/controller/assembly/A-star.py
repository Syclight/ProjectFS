from source.controller.assembly.Shape import Rectangle
from source.util.Math2d import point2


def heuristic(a, b):
    return abs(a.i - b.i) + abs(a.j - b.j)


class Spot:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbors = []
        self.previous = None
        self.wall = False

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
    def __init__(self, rect, cols, rows, start, end):
        self.__grid = []
        self.rect = rect
        self.cols, self.rows = cols, rows
        self.unit_w, self.unit_h = self.rect.w / self.cols, self.rect.w / self.rows
        self.__openSet, self.__closeSet = [], []
        self.__initArea()
        self.start = self.__grid[start[0]][start[1]]
        self.end = self.__grid[end[0]][end[1]]
        self.__openSet.append(self.start)
        self.__done = False
        self.__noSolution = False
        self.__resList = []

    def __initArea(self):
        for i in range(0, self.cols):
            self.__grid.append([])

        for i in range(0, self.cols):
            for j in range(0, self.rows):
                self.__grid[i].append(Spot(i, j))

        for i in range(0, self.cols):
            for j in range(0, self.rows):
                self.__grid[i][j].addNeighbors(self.cols, self.rows, self.__grid)

    def addWall(self, x, y):
        if self.start.i == x and self.start.j == y or self.end.i == x and self.end.j == y:
            raise Exception('({}, {}) shouldnt be startPos or endPos'.format(x, y))
        self.__grid[x][y].wall = True

    def addWalls(self, pos_list):
        for x, y in pos_list:
            self.addWall(x, y)

    def removeWall(self, x, y):
        self.__grid[x][y].wall = False

    def removeWalls(self, pos_list):
        for x, y in pos_list:
            self.removeWall(x, y)

    def setStart(self, start):
        self.__openSet.clear()
        self.start = self.__grid[start[0]][start[1]]
        self.__openSet.append(self.start)

    def setEnd(self, end):
        self.end = self.__grid[end[0]][end[1]]

    def run(self):
        while not self.__done:

            current = None
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


area = AStartArea(Rectangle(0, 0, 500, 500), 10, 10, (0, 0), (9, 9))
area.addWall(4, 4)
area.addWalls([(4, 4), (3, 3), (6, 5)])
print(area.run())
