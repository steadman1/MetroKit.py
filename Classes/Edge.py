import os
import sys
from math import sqrt, atan2
from typing import TYPE_CHECKING

absolute_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(absolute_path)

if TYPE_CHECKING:
    from Direction import Direction
    from Point import Point

# a single edge between two vertices
class Edge:
    def __init__(self, start: Point, end: Point) -> None:
        self.start = start
        self.end = end
        
        if start.y == end.y:
            self.direction = Direction.NORTH_SOUTH_BI
        elif start.x == end.x:
            self.direction = Direction.WEST_EAST_BI
        elif (end.x - start.x) == (end.y - start.y):
            self.direction = Direction.NORTH_WEST_BI
        elif (end.x - start.x) == -(end.y - start.y):
            self.direction = Direction.NORTH_EAST_BI
        else:
            raise Exception("Invalid edge start, end pair")
    
    def get_direction(self) -> Direction:
        return self.direction
    
    def get_length(self) -> float:
        return sqrt( pow(self.end.x - self.start.x, 2) + pow(self.start.y - self.end.y, 2) )
    
    def get_angle_rad(self) -> float:
        return atan2(self.end.y - self.start.y, self.end.x - self.start.x)