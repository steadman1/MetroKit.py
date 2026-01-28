import os
import sys
from threading import ExceptHookArgs

absolute_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(absolute_path)

from Direction import Direction
from Point import Point

class Edge:
    def __init__(self, start: Point, end: Point) -> None:
        if start.y == end.y:
            self.direction = Direction.NS
        elif start.x == end.x:
            self.direction = Direction.WE
        elif (end.x - start.x) == (end.y - start.y):
            self.direction = Direction.NW
        elif (end.x - start.x) == -(end.y - start.y):
            self.direction = Direction.NE
        else:
            raise Exception("Invalid edge start, end pair")
        

class Line:
    def __init__(self, start: Point, end: Point) -> None:
        self.anchors = []
        self.start = start
        self.end = end