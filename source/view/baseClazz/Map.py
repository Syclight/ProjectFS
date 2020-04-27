import pygame

from source.core.assembly.A_star import AStarArea
from source.core.math.Shape import Rectangle


class Map2d:
    def __init__(self):
        self.length, self.width = 0, 0
        self.show_length, self.show_width = 0, 0
        self.A_Map = None
        self.__surface = None
        self.isInit = False

    def init(self, length, width, show_length, show_width, pathfinding_unit):
        self.width, self.length = width, length
        self.show_length, self.show_width = show_length, show_width
        self.A_Map = AStarArea(Rectangle(0, 0, self.show_length, self.show_width), self.show_length / pathfinding_unit,
                               self.show_length / pathfinding_unit)
        self.__surface = pygame.Surface((self.length, self.width)).convert()
        self.isInit = True

    def setAstarMap(self, map):
        if not isinstance(map, AStarArea):
            return
        self.A_Map = map

    def show(self, surface):
        return self.__surface

