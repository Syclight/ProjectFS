import random

import pygame

from source.core.const.Const import gl_Font
from source.util.ToolsFuc import centeredXPos
from source.view.baseClazz.Scene import Scene
from source.view.element.Elements import TextElement


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
        if random.uniform(0, 1) < 0.5:
            self.wall = True

    def show(self, surface, col, w, h):
        color = col
        if self.wall:
            color = (0, 0, 0)
            # pygame.draw.rect(surface, color, (self.i * w, self.j * h, w - 1, h - 1), 0)
            # pygame.draw.circle(surface, color, (self.i * w + w / 2, self.j * h + h / 2), (w / 2), 1)
        pygame.draw.rect(surface, color, (self.i * w, self.j * h, w - 1, h - 1), 0)

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


class AstartTest(Scene):
    def __init__(self, screen, config, time):
        super(AstartTest, self).__init__(screen, config, time)
        self.cols, self.rows = 100, 100
        self.grid = []
        self.openSet, self.closeSet = [], []
        self.start, self.end = None, None
        self.w, self.h = screen.get_width() / self.cols, screen.get_height() / self.rows
        self.path = []
        self.done = False
        self.noSolution = False
        self.points = []
        self.__E_TEXT = TextElement(pygame.Rect(centeredXPos(self.width, 220), 260, 220, 60), '', gl_Font, 50,
                                    (255, 255, 0), 1)

        for i in range(0, self.cols):
            self.grid.append([])

        for i in range(0, self.cols):
            for j in range(0, self.rows):
                self.grid[i].append(Spot(i, j))

        for i in range(0, self.cols):
            for j in range(0, self.rows):
                self.grid[i][j].addNeighbors(self.cols, self.rows, self.grid)

        self.start = self.grid[0][0]
        self.end = self.grid[self.cols - 1][self.rows - 1]
        self.start.wall = False
        self.end.wall = False
        self.openSet.append(self.start)

    def draw(self):
        current = None
        if len(self.openSet) > 0:
            winner = 0
            for i in range(0, len(self.openSet)):
                if self.openSet[i].f < self.openSet[winner].f:
                    winner = i

            current = self.openSet[winner]

            if current == self.end:
                self.done = True

            if not self.done:
                self.openSet.remove(current)
                self.closeSet.append(current)

                neighbors = current.neighbors
                for i in range(0, len(neighbors)):
                    neighbor = neighbors[i]
                    if neighbor not in self.closeSet and not neighbor.wall:
                        tempG = current.g + 1
                        newPath = False
                        if neighbor in self.openSet:
                            if tempG < neighbor.g:
                                neighbor.g = tempG
                                newPath = True
                        else:
                            neighbor.g = tempG
                            newPath = True
                            self.openSet.append(neighbor)
                        if newPath:
                            neighbor.h = heuristic(neighbor, self.end)
                            neighbor.f = neighbor.g + neighbor.h
                            neighbor.previous = current
        else:
            self.done = True
            self.__E_TEXT.setText('寻路失败')
            self.noSolution = True

        # self.screen.fill((255, 255, 255))

        for i in range(0, self.cols):
            for j in range(0, self.rows):
                self.grid[i][j].show(self.screen, (255, 255, 255), self.w, self.h)

        for i in range(0, len(self.openSet)):
            self.openSet[i].show(self.screen, (0, 255, 0), self.w, self.h)

        for i in range(0, len(self.closeSet)):
            self.closeSet[i].show(self.screen, (255, 0, 0), self.w, self.h)

        if not self.done:
            self.path.clear()
            temp = current
            self.path.append(temp)
            while temp is not None and temp.previous:
                self.path.append(temp.previous)
                temp = temp.previous
        elif self.done and not self.noSolution:
            self.path.append(self.end)
            self.__E_TEXT.setText('寻路成功')


        for i in range(0, len(self.path)):
            e = self.path[i]
            if e is not None:
                e.show(self.screen, (0, 0, 255), self.w, self.h)

        self.__E_TEXT.draw(self.screen)

        # for i in range(0, len(pathN)):
        #     e = pathN[i]
        #     if e is not None:
        #         self.points.append([e.i * self.w + self.w / 2, e.j * self.h + self.h / 2])
        #         if len(self.points) > 1:
        #             print(self.points)
        #             pygame.draw.line(self.screen, (250, 0, 100), self.points[0], self.points[1], 5)
        #             self.points.pop(0)
